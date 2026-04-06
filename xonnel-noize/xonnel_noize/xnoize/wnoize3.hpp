#pragma once

#include <cstddef>
#include <cstdint>

class WNoize3
{
public:
    explicit WNoize3(std::uint32_t seed = 0);

    void generate(
        float* out,
        std::size_t w,
        std::size_t h,
        std::size_t d,
        float scale = 64.0f,
        std::size_t octs = 1,
        float pers = 0.5f,
        float lacu = 2.0f,
        float offx = 0.0f,
        float offy = 0.0f,
        float offz = 0.0f,
        float norm0 = 0.0f,
        float norm1 = 1.0f
    ) const;

private:
    std::uint32_t seed_;

    static int fastfloor(float x);
    std::uint32_t hash(std::int32_t x, std::int32_t y, std::int32_t z) const;
    float rand01(std::uint32_t v) const;
    float sample(float x, float y, float z) const;
};

extern "C"
{
    __declspec(dllexport) void wnoize3(
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
    );
}