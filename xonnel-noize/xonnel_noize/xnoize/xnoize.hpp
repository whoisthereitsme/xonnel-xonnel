#pragma once

#include <cstddef>
#include <cstdint>

namespace xnoize
{
    class XNoize
    {
    public:
        explicit XNoize(std::uint32_t seed = 0);

        void perlin(
            float* out,
            std::size_t w,
            std::size_t h,
            float scale = 64.0f,
            std::size_t octs = 1,
            float pers = 0.5f,
            float lacu = 2.0f,
            float offx = 0.0f,
            float offy = 0.0f,
            float norm0 = 0.0f,
            float norm1 = 1.0f
        ) const;

    private:
        std::uint8_t perm_[512];

        static float fade(float t);
        static float lerp(float a, float b, float t);
        static float grad(int hash, float x, float y);

        void build_perm(std::uint32_t seed);
        float sample(float x, float y) const;
    };
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
    );
}