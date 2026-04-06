#include "pnoize3.hpp"

#include <algorithm>
#include <cmath>
#include <memory>
#include <mutex>
#include <random>
#include <stdexcept>
#include <thread>
#include <unordered_map>
#include <vector>



PNoize3::PNoize3(std::uint32_t seed)
{
    build_perm(seed);
}



void PNoize3::build_perm(std::uint32_t seed)
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



float PNoize3::fade(float t)
{
    return t * t * t * (t * (t * 6.0f - 15.0f) + 10.0f);
}



float PNoize3::lerp(float a, float b, float t)
{
    return a + t * (b - a);
}



float PNoize3::grad(int hash, float x, float y, float z)
{
    switch (hash & 15)
    {
        case  0: return  x + y;
        case  1: return -x + y;
        case  2: return  x - y;
        case  3: return -x - y;
        case  4: return  x + z;
        case  5: return -x + z;
        case  6: return  x - z;
        case  7: return -x - z;
        case  8: return  y + z;
        case  9: return -y + z;
        case 10: return  y - z;
        case 11: return -y - z;
        case 12: return  x + y;
        case 13: return -x + y;
        case 14: return -y + z;
        case 15: return -y - z;
        default: return 0.0f;
    }
}



float PNoize3::sample(float x, float y, float z) const
{
    const int xi0 = static_cast<int>(std::floor(x)) & 255;
    const int yi0 = static_cast<int>(std::floor(y)) & 255;
    const int zi0 = static_cast<int>(std::floor(z)) & 255;

    const int xi1 = (xi0 + 1) & 255;
    const int yi1 = (yi0 + 1) & 255;
    const int zi1 = (zi0 + 1) & 255;

    const float xf0 = x - std::floor(x);
    const float yf0 = y - std::floor(y);
    const float zf0 = z - std::floor(z);

    const float xf1 = xf0 - 1.0f;
    const float yf1 = yf0 - 1.0f;
    const float zf1 = zf0 - 1.0f;

    const float u = fade(xf0);
    const float v = fade(yf0);
    const float w = fade(zf0);

    const int aaa = perm_[perm_[perm_[xi0] + yi0] + zi0];
    const int aab = perm_[perm_[perm_[xi0] + yi0] + zi1];
    const int aba = perm_[perm_[perm_[xi0] + yi1] + zi0];
    const int abb = perm_[perm_[perm_[xi0] + yi1] + zi1];
    const int baa = perm_[perm_[perm_[xi1] + yi0] + zi0];
    const int bab = perm_[perm_[perm_[xi1] + yi0] + zi1];
    const int bba = perm_[perm_[perm_[xi1] + yi1] + zi0];
    const int bbb = perm_[perm_[perm_[xi1] + yi1] + zi1];

    const float x1 = lerp(grad(aaa, xf0, yf0, zf0), grad(baa, xf1, yf0, zf0), u);
    const float x2 = lerp(grad(aba, xf0, yf1, zf0), grad(bba, xf1, yf1, zf0), u);
    const float y1 = lerp(x1, x2, v);

    const float x3 = lerp(grad(aab, xf0, yf0, zf1), grad(bab, xf1, yf0, zf1), u);
    const float x4 = lerp(grad(abb, xf0, yf1, zf1), grad(bbb, xf1, yf1, zf1), u);
    const float y2 = lerp(x3, x4, v);

    return lerp(y1, y2, w);
}



void PNoize3::generate(
    float* out,
    std::size_t w,
    std::size_t h,
    std::size_t d,
    float scale,
    std::size_t octs,
    float pers,
    float lacu,
    float offx,
    float offy,
    float offz,
    float norm0,
    float norm1
) const
{
    if (out == nullptr) throw std::invalid_argument("out is null");
    if (w == 0 || h == 0 || d == 0) throw std::invalid_argument("w/h/d invalid");
    if (scale <= 0.0f) throw std::invalid_argument("scale invalid");
    if (octs == 0) throw std::invalid_argument("octs invalid");
    if (lacu <= 0.0f) throw std::invalid_argument("lacu invalid");

    const std::size_t hw = std::thread::hardware_concurrency();
    const std::size_t nthreads = hw > 0 ? hw : 4;

    const std::size_t slices_per_thread = (d + nthreads - 1) / nthreads;

    std::vector<float> mins(nthreads);
    std::vector<float> maxs(nthreads);
    std::vector<std::thread> threads;

    threads.reserve(nthreads);



    auto worker = [&](std::size_t tid, std::size_t z0, std::size_t z1)
    {
        bool first = true;
        float mn = 0.0f;
        float mx = 0.0f;

        for (std::size_t z = z0; z < z1; ++z)
        {
            for (std::size_t y = 0; y < h; ++y)
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
                        const float sz = (static_cast<float>(z) + offz) / scale * freq;

                        val += sample(sx, sy, sz) * amp;
                        amp_sum += amp;

                        amp *= pers;
                        freq *= lacu;
                    }

                    if (amp_sum > 0.0f)
                    {
                        val /= amp_sum;
                    }

                    const std::size_t i = (z * h + y) * w + x;
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
        }

        mins[tid] = mn;
        maxs[tid] = mx;
    };



    for (std::size_t tid = 0; tid < nthreads; ++tid)
    {
        const std::size_t z0 = tid * slices_per_thread;
        const std::size_t z1 = std::min(z0 + slices_per_thread, d);

        if (z0 >= z1)
        {
            mins[tid] = 0.0f;
            maxs[tid] = 0.0f;
            continue;
        }

        threads.emplace_back(worker, tid, z0, z1);
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
        const std::size_t z0 = tid * slices_per_thread;
        const std::size_t z1 = std::min(z0 + slices_per_thread, d);

        if (z0 >= z1) continue;

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
    const std::size_t size = w * h * d;

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
    __declspec(dllexport) void pnoize3(
        float* out,
        std::size_t w,
        std::size_t h,
        std::size_t d,
        std::uint32_t seed,
        float scale,
        std::size_t octs,
        float pers,
        float lacu,
        float offx,
        float offy,
        float offz,
        float norm0,
        float norm1
    )
    {
        static std::unordered_map<std::uint32_t, std::shared_ptr<PNoize3>> cache;
        static std::mutex mutex;

        std::shared_ptr<PNoize3> inst;

        {
            std::lock_guard<std::mutex> lock(mutex);

            auto it = cache.find(seed);

            if (it == cache.end())
            {
                inst = std::make_shared<PNoize3>(seed);
                cache.emplace(seed, inst);
            }
            else
            {
                inst = it->second;
            }
        }

        inst->generate(out, w, h, d, scale, octs, pers, lacu, offx, offy, offz, norm0, norm1);
    }
}