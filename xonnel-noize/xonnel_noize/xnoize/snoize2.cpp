#include "snoize2.hpp"

#include <algorithm>
#include <cmath>
#include <memory>
#include <mutex>
#include <random>
#include <stdexcept>
#include <thread>
#include <unordered_map>
#include <vector>



static const int SNOIZE2_GRADS[12][2] =
{
    {  1,  1 }, { -1,  1 }, {  1, -1 }, { -1, -1 },
    {  1,  0 }, { -1,  0 }, {  1,  0 }, { -1,  0 },
    {  0,  1 }, {  0, -1 }, {  0,  1 }, {  0, -1 }
};



SNoize2::SNoize2(std::uint32_t seed)
{
    build_perm(seed);
}



void SNoize2::build_perm(std::uint32_t seed)
{
    std::uint8_t base[256];

    for (int i = 0; i < 256; ++i)
    {
        base[i] = static_cast<std::uint8_t>(i);
    }

    std::mt19937 rng(seed);
    std::shuffle(std::begin(base), std::end(base), rng);

    for (int i = 0; i < 256; ++i)
    {
        perm_[i] = base[i];
        perm_[256 + i] = base[i];
    }
}



int SNoize2::fastfloor(float x)
{
    const int i = static_cast<int>(x);
    return (x < static_cast<float>(i)) ? (i - 1) : i;
}



float SNoize2::dot(const int* g, float x, float y)
{
    return static_cast<float>(g[0]) * x + static_cast<float>(g[1]) * y;
}



float SNoize2::sample(float x, float y) const
{
    constexpr float F2 = 0.36602540378443864676f;   // 0.5 * (sqrt(3) - 1)
    constexpr float G2 = 0.21132486540518711775f;   // (3 - sqrt(3)) / 6

    const float s = (x + y) * F2;
    const int i = fastfloor(x + s);
    const int j = fastfloor(y + s);

    const float t = static_cast<float>(i + j) * G2;
    const float X0 = static_cast<float>(i) - t;
    const float Y0 = static_cast<float>(j) - t;

    const float x0 = x - X0;
    const float y0 = y - Y0;

    int i1;
    int j1;

    if (x0 > y0)
    {
        i1 = 1;
        j1 = 0;
    }
    else
    {
        i1 = 0;
        j1 = 1;
    }

    const float x1 = x0 - static_cast<float>(i1) + G2;
    const float y1 = y0 - static_cast<float>(j1) + G2;
    const float x2 = x0 - 1.0f + 2.0f * G2;
    const float y2 = y0 - 1.0f + 2.0f * G2;

    const int ii = i & 255;
    const int jj = j & 255;

    const int gi0 = perm_[ii + perm_[jj]] % 12;
    const int gi1 = perm_[ii + i1 + perm_[jj + j1]] % 12;
    const int gi2 = perm_[ii + 1 + perm_[jj + 1]] % 12;

    float n0 = 0.0f;
    float n1 = 0.0f;
    float n2 = 0.0f;

    float t0 = 0.5f - x0 * x0 - y0 * y0;
    if (t0 > 0.0f)
    {
        t0 *= t0;
        n0 = t0 * t0 * dot(SNOIZE2_GRADS[gi0], x0, y0);
    }

    float t1 = 0.5f - x1 * x1 - y1 * y1;
    if (t1 > 0.0f)
    {
        t1 *= t1;
        n1 = t1 * t1 * dot(SNOIZE2_GRADS[gi1], x1, y1);
    }

    float t2 = 0.5f - x2 * x2 - y2 * y2;
    if (t2 > 0.0f)
    {
        t2 *= t2;
        n2 = t2 * t2 * dot(SNOIZE2_GRADS[gi2], x2, y2);
    }

    return 70.0f * (n0 + n1 + n2);
}



void SNoize2::generate(
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
    __declspec(dllexport) void snoize2(
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
        static std::unordered_map<std::uint32_t, std::shared_ptr<SNoize2>> cache;
        static std::mutex mutex;

        std::shared_ptr<SNoize2> inst;

        {
            std::lock_guard<std::mutex> lock(mutex);

            auto it = cache.find(seed);

            if (it == cache.end())
            {
                inst = std::make_shared<SNoize2>(seed);
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