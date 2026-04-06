#include "wnoize2.hpp"

#include <algorithm>
#include <cmath>
#include <cstdint>
#include <memory>
#include <mutex>
#include <stdexcept>
#include <thread>
#include <unordered_map>
#include <vector>



WNoize2::WNoize2(std::uint32_t seed)
    : seed_(seed)
{
}



int WNoize2::fastfloor(float x)
{
    const int i = static_cast<int>(x);
    return (x < static_cast<float>(i)) ? (i - 1) : i;
}



std::uint32_t WNoize2::hash(std::int32_t x, std::int32_t y) const
{
    std::uint32_t h = seed_;

    h ^= static_cast<std::uint32_t>(x) * 0x27d4eb2dU;
    h ^= static_cast<std::uint32_t>(y) * 0x85ebca6bU;

    h ^= h >> 15;
    h *= 0x2c1b3c6dU;
    h ^= h >> 12;
    h *= 0x297a2d39U;
    h ^= h >> 15;

    return h;
}



float WNoize2::rand01(std::uint32_t v) const
{
    return static_cast<float>(v) / static_cast<float>(0xffffffffU);
}



float WNoize2::sample(float x, float y) const
{
    const int ix = fastfloor(x);
    const int iy = fastfloor(y);

    float best = 1e30f;

    for (int oy = -1; oy <= 1; ++oy)
    {
        for (int ox = -1; ox <= 1; ++ox)
        {
            const int cx = ix + ox;
            const int cy = iy + oy;

            const std::uint32_t h0 = hash(cx, cy);
            const std::uint32_t h1 = hash(cx ^ 0x68bc21eb, cy ^ 0x02e5be93);

            const float fx = static_cast<float>(cx) + rand01(h0);
            const float fy = static_cast<float>(cy) + rand01(h1);

            const float dx = fx - x;
            const float dy = fy - y;

            const float dist = std::sqrt(dx * dx + dy * dy);

            if (dist < best)
            {
                best = dist;
            }
        }
    }

    return best;
}



void WNoize2::generate(
    float* out,
    std::size_t w,
    std::size_t h,
    float scale,
    std::size_t octs,
    float pers,
    float lacu,
    float offx,
    float offy,
    float norm0,
    float norm1
) const
{
    if (out == nullptr) throw std::invalid_argument("out is null");
    if (w == 0 || h == 0) throw std::invalid_argument("w/h invalid");
    if (scale <= 0.0f) throw std::invalid_argument("scale invalid");
    if (octs == 0) throw std::invalid_argument("octs invalid");
    if (lacu <= 0.0f) throw std::invalid_argument("lacu invalid");

    const std::size_t hw = std::thread::hardware_concurrency();
    const std::size_t nthreads = hw > 0 ? hw : 4;

    const std::size_t rows_per_thread = (h + nthreads - 1) / nthreads;

    std::vector<float> mins(nthreads);
    std::vector<float> maxs(nthreads);
    std::vector<std::thread> threads;

    threads.reserve(nthreads);



    auto worker = [&](std::size_t tid, std::size_t y0, std::size_t y1)
    {
        bool first = true;
        float mn = 0.0f;
        float mx = 0.0f;

        for (std::size_t y = y0; y < y1; ++y)
        {
            for (std::size_t x = 0; x < w; ++x)
            {
                float amp = 1.0f;
                float freq = 1.0f;
                float val = 0.0f;
                float amp_sum = 0.0f;

                for (std::size_t o = 0; o < octs; ++o)
                {
                    const float sx = (static_cast<float>(x) + offx) / scale * freq;
                    const float sy = (static_cast<float>(y) + offy) / scale * freq;

                    val += sample(sx, sy) * amp;
                    amp_sum += amp;

                    amp *= pers;
                    freq *= lacu;
                }

                if (amp_sum > 0.0f)
                {
                    val /= amp_sum;
                }

                const std::size_t i = y * w + x;
                out[i] = val;

                if (first)
                {
                    mn = val;
                    mx = val;
                    first = false;
                }
                else
                {
                    if (val < mn) mn = val;
                    if (val > mx) mx = val;
                }
            }
        }

        mins[tid] = mn;
        maxs[tid] = mx;
    };



    for (std::size_t tid = 0; tid < nthreads; ++tid)
    {
        const std::size_t y0 = tid * rows_per_thread;
        const std::size_t y1 = std::min(y0 + rows_per_thread, h);

        if (y0 >= y1)
        {
            mins[tid] = 0.0f;
            maxs[tid] = 0.0f;
            continue;
        }

        threads.emplace_back(worker, tid, y0, y1);
    }

    for (auto& t : threads)
    {
        t.join();
    }



    bool first = true;
    float mn = 0.0f;
    float mx = 0.0f;

    for (std::size_t tid = 0; tid < nthreads; ++tid)
    {
        const std::size_t y0 = tid * rows_per_thread;
        const std::size_t y1 = std::min(y0 + rows_per_thread, h);

        if (y0 >= y1) continue;

        if (first)
        {
            mn = mins[tid];
            mx = maxs[tid];
            first = false;
        }
        else
        {
            if (mins[tid] < mn) mn = mins[tid];
            if (maxs[tid] > mx) mx = maxs[tid];
        }
    }



    const float src_rng = mx - mn;
    const float dst_rng = norm1 - norm0;
    const std::size_t size = w * h;

    if (src_rng > 0.0f)
    {
        for (std::size_t i = 0; i < size; ++i)
        {
            out[i] = norm0 + ((out[i] - mn) / src_rng) * dst_rng;
        }
    }
    else
    {
        const float mid = (norm0 + norm1) * 0.5f;

        for (std::size_t i = 0; i < size; ++i)
        {
            out[i] = mid;
        }
    }
}



extern "C"
{
    __declspec(dllexport) void wnoize2(
        float* out,
        std::size_t w,
        std::size_t h,
        std::uint32_t seed,
        float scale,
        std::size_t octs,
        float pers,
        float lacu,
        float offx,
        float offy,
        float norm0,
        float norm1
    )
    {
        static std::unordered_map<std::uint32_t, std::shared_ptr<WNoize2>> cache;
        static std::mutex mutex;

        std::shared_ptr<WNoize2> inst;

        {
            std::lock_guard<std::mutex> lock(mutex);

            auto it = cache.find(seed);

            if (it == cache.end())
            {
                inst = std::make_shared<WNoize2>(seed);
                cache.emplace(seed, inst);
            }
            else
            {
                inst = it->second;
            }
        }

        inst->generate(out, w, h, scale, octs, pers, lacu, offx, offy, norm0, norm1);
    }
}