#include "xnoize.hpp"

#include <algorithm>
#include <cmath>
#include <random>
#include <stdexcept>
#include <unordered_map>
#include <memory>
#include <mutex>
#include <thread>
#include <vector>

namespace xnoize
{
    XNoize::XNoize(std::uint32_t seed)
    {
        build_perm(seed);
    }

    void XNoize::build_perm(std::uint32_t seed)
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

    float XNoize::fade(float t)
    {
        return t * t * t * (t * (t * 6.0f - 15.0f) + 10.0f);
    }

    float XNoize::lerp(float a, float b, float t)
    {
        return a + t * (b - a);
    }

    float XNoize::grad(int hash, float x, float y)
    {
        switch (hash & 7)
        {
            case 0: return  x + y;
            case 1: return -x + y;
            case 2: return  x - y;
            case 3: return -x - y;
            case 4: return  x;
            case 5: return -x;
            case 6: return  y;
            case 7: return -y;
            default: return 0.0f;
        }
    }

    float XNoize::sample(float x, float y) const
    {
        const int xi0 = static_cast<int>(std::floor(x)) & 255;
        const int yi0 = static_cast<int>(std::floor(y)) & 255;
        const int xi1 = (xi0 + 1) & 255;
        const int yi1 = (yi0 + 1) & 255;

        const float xf0 = x - std::floor(x);
        const float yf0 = y - std::floor(y);
        const float xf1 = xf0 - 1.0f;
        const float yf1 = yf0 - 1.0f;

        const float u = fade(xf0);
        const float v = fade(yf0);

        const int aa = perm_[perm_[xi0] + yi0];
        const int ab = perm_[perm_[xi0] + yi1];
        const int ba = perm_[perm_[xi1] + yi0];
        const int bb = perm_[perm_[xi1] + yi1];

        const float x1 = lerp(grad(aa, xf0, yf0), grad(ba, xf1, yf0), u);
        const float x2 = lerp(grad(ab, xf0, yf1), grad(bb, xf1, yf1), u);

        return lerp(x1, x2, v);
    }

    void XNoize::perlin(
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
        if (w == 0 || h == 0) throw std::invalid_argument("w and h must be > 0");
        if (scale <= 0.0f) throw std::invalid_argument("scale must be > 0");
        if (octs == 0) throw std::invalid_argument("octs must be > 0");
        if (lacu <= 0.0f) throw std::invalid_argument("lacu must be > 0");

        const std::size_t nthreads_hw = std::thread::hardware_concurrency();
        const std::size_t nthreads = nthreads_hw > 0 ? nthreads_hw : 4;
        const std::size_t rows_per_thread = (h + nthreads - 1) / nthreads;

        std::vector<float> mins(nthreads, 0.0f);
        std::vector<float> maxs(nthreads, 0.0f);
        std::vector<std::thread> threads;

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

                    for (std::size_t oct = 0; oct < octs; ++oct)
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

        const float rng = mx - mn;
        const float norm_rng = norm1 - norm0;
        const std::size_t size = w * h;

        if (rng > 0.0f)
        {
            for (std::size_t i = 0; i < size; ++i)
            {
                out[i] = norm0 + ((out[i] - mn) / rng) * norm_rng;
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
}

extern "C"
{
    __declspec(dllexport) void xnoize_perlin(
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
        static std::unordered_map<std::uint32_t, std::shared_ptr<xnoize::XNoize>> cache;
        static std::mutex cache_mutex;

        std::shared_ptr<xnoize::XNoize> noize;

        {
            std::lock_guard<std::mutex> lock(cache_mutex);

            auto it = cache.find(seed);
            if (it == cache.end())
            {
                noize = std::make_shared<xnoize::XNoize>(seed);
                cache.emplace(seed, noize);
            }
            else
            {
                noize = it->second;
            }
        }

        noize->perlin(out, w, h, scale, octs, pers, lacu, offx, offy, norm0, norm1);
    }
}