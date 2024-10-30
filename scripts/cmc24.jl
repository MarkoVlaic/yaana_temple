# Computational Modeling Challenge 2024
# CMC24 solution evaluation script
# Author: Hrvoje Abraham, hrvoje.abraham@avl.com

using FileIO
using ImageIO
using Measures
using Plots; gr()
using UUIDs

temple_string =
#1  2  3  4  5  6  7  8  9  0  1  2  3  4  5  6  7  8  9  0
"O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O
 O  .  .  .  .  O  .  .  .  .  .  .  .  .  O  .  .  .  .  O
 O  .  .  .  .  .  .  .  O  .  .  O  .  .  .  .  .  .  .  O
 O  .  .  .  .  .  O  .  .  .  .  .  .  O  .  .  .  .  .  O
 O  .  .  O  .  .  .  .  .  O  O  .  .  .  .  .  O  .  .  O
 O  O  .  .  .  .  .  .  .  O  O  .  .  .  .  .  .  .  O  O
 O  .  .  .  O  .  .  .  .  .  .  .  .  .  .  O  .  .  .  O
 O  .  .  .  .  .  .  O  .  .  .  .  O  .  .  .  .  .  .  O
 O  .  .  .  .  .  .  .  .  O  O  .  .  .  .  .  .  .  .  O
 O  .  O  .  .  O  O  .  .  .  .  .  .  O  O  .  .  O  .  O
 O  .  O  .  .  O  O  .  .  .  .  .  .  O  O  .  .  O  .  O
 O  .  .  .  .  .  .  .  .  O  O  .  .  .  .  .  .  .  .  O
 O  .  .  .  .  .  .  O  .  .  .  .  O  .  .  .  .  .  .  O
 O  .  .  .  O  .  .  .  .  .  .  .  .  .  .  O  .  .  .  O
 O  O  .  .  .  .  .  .  .  O  O  .  .  .  .  .  .  .  O  O
 O  .  .  O  .  .  .  .  .  O  O  .  .  .  .  .  O  .  .  O
 O  .  .  .  .  .  O  .  .  .  .  .  .  O  .  .  .  .  .  O
 O  .  .  .  .  .  .  .  O  .  .  O  .  .  .  .  .  .  .  O
 O  .  .  .  .  O  .  .  .  .  .  .  .  .  O  .  .  .  .  O
 O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O"

block_size = 1
mirror_length = 0.5
light_halfwidth = 1
ε = 1e-12

"""Float64 infinity"""
∞ = Inf

"""
    ⋅(v, w)

Dot product of two 2D vectors.
"""
function ⋅(v, w)
    return v[1] * w[1] + v[2] * w[2]
end

"""
    ×(v, w)

Cross product of two 2D vectors.
"""
function ×(v, w)
    return v[1] * w[2] - v[2] * w[1]
end

"""Last 12 digits of hexadecimal format of the input integer."""
function hex12(x::Integer)
    return last(string(x, base=16), 12)
end

"""
    Convert integer into string with digit grouping.

    E.g. 1234567 => "1,234,567"
"""
function commas(num::Integer)
    str = string(num)
    return replace(str, r"(?<=[0-9])(?=(?:[0-9]{3})+(?![0-9]))" => ",")
end

function load_temple(temple_string, block_size)
    # println(stderr, " " * temple_string)
    rows = split(replace(strip(temple_string), " " => ""), '\n')
    temple_shape = length(rows[1]), length(rows)

    temple = Set()
    for (j, row) ∈ enumerate(rows)
        for (i, c) ∈ enumerate(row)
            if c == 'O'
                x = (i - 1) * block_size
                y = temple_shape[2] - j * block_size
                
                v1 = [x, y]
                v2 = [x + block_size, y]
                v3 = [x + block_size, y + block_size]
                v4 = [x, y + block_size]

                block = (
                    v1 = v1,  # bottom left corner
                    v2 = v2,
                    v3 = v3,  # up right corner
                    v4 = v4,

                    s1 = (v1, block_size, 0),
                    s2 = (v2, block_size, π/2),
                    s3 = (v3, block_size, π),
                    s4 = (v4, block_size, 3π/2),
                )
                
                push!(temple, block)
            end
        end
    end
    # display(temple)

    println(stderr, "The temple of size $temple_shape is loaded.")

    return (
        blocks = temple,
        shape = temple_shape,
        size = block_size .* temple_shape
    )
end

function load_solution(cmc24_solution, mirror_length)
    if size(cmc24_solution) ≠ (9, 3)
        println(stderr, "ERROR! The solution isn't 9x3 size matrix.")
        finalize()
    end

    if !(eltype(cmc24_solution) <: Number)
        println(stderr, "ERROR! The solution contains non-numerical inputs.")
        finalize()
    end

    try
        cmc24_solution = float(cmc24_solution)
    catch
        println(stderr, "ERROR! The solution can't be converted to double precision floating point format.")
        finalize()
    end

    # preprocess the lamp
    α = cmc24_solution[1, 3]
    lamp = (
        v = cmc24_solution[1, 1:2],
        α = α,
        e = [cos(α), sin(α)]
    )

    # preprocess the mirrors
    mirrors = []
    for m ∈ 1 : 8
        α = cmc24_solution[m + 1, 3]
        
        v = cmc24_solution[m + 1, 1:2]
        e = [cos(α),  sin(α)]
        n = [-sin(α), cos(α)]  # normal

        mirror = (
            v1 = v,
            v2 = v + mirror_length * e,
            s = (v, mirror_length, α),
            α = α,
            e = e,
            n = n,
        )

        push!(mirrors, mirror)
    end

    println(stderr, "The solution is loaded.")

    return (lamp, mirrors)
end

function point_in_block(temple, point)
    for cell ∈ temple.blocks
        # if the point is within bottom-left and top-right vertex
        if all(cell.v1 .≤ point .≤ cell.v3)
            return true
        end
    end

    return false
end

function point_sector(temple, point)
    sx = floor(Int, 3 * point[1] / temple.size[1])
    sy = floor(Int, 3 * point[2] / temple.size[2])

    return 3 * sy + sx + 1
end

function ray_ray_intersection(ray1, ray2)
    (p, r) = ray1
    (q, s) = ray2

    rs = r × s
    qpr = (q - p) × r

    # CASE 1 - rays are collinear and maybe overlap
    if (rs == 0) && (qpr == 0)
        t0 = (q - p) ⋅ r / (r ⋅ r)
        t1 = (q + s - p) ⋅ r / (r ⋅ r)
        return (1, t0, t1)
    end

    # CASE 2 - rays are parallel so they don't intersect
    if (rs == 0) && (qpr ≠ 0)
        return (2, 0, 0)
    end

    # CASE 3 - rays intersect
    qps = (q - p) × s
    t = qps / rs
    u = qpr / rs
    if (rs ≠ 0) && (t ≥ 0) && (u ≥ 0)
        return (3, t, u)
    end

    # CASE 4 - rays don't intersect
    return (4, 0, 0)
end

function ray_segment_intersection(ray, segment)
    (p, r) = ray
    (q, l, β) = segment

    s = l * [cos(β), sin(β)]

    (case, t, u) = ray_ray_intersection((p, r), (q, s))

    # CASE 1 - No intersection
    if case == 1 && t < 0 && u < 0            return (1, 0, 0) end
    if case == 2                              return (1, 0, 0) end
    if case == 3 && (t ≤ 0 || u < 0 || u > 1) return (1, 0, 0) end
    if case == 4                              return (1, 0, 0) end

    # CASE 2 - Ray and segment are collinear and they intersect
    if case == 1
        if t > 0 && u ≥ 0 return (2, min(t, u), 0) end
        if t ≥ 0          return (2, t, 0)         end
        if u ≥ 0          return (2, 0, 0)         end
    end

    # CASE 3 - Ray and segment intersect in ordinary way
    return (3, t, u)
end

function segment_segment_intersection(segment1, segment2)
    (p, la, α) = segment1
    (q, lb, β) = segment2

    r = la * [cos(α), sin(α)]
    s = lb * [cos(β), sin(β)]

    (case, t, u) = ray_ray_intersection((p, r), (q, s))

    if case == 1 && r ⋅ s > 0 && t ≤ u && (0 ≤ t ≤ 1 || 0 ≤ u ≤ 1)
        return true
    end

    if case == 1 && r ⋅ s < 0 && t ≥ u && (0 ≤ t ≤ 1 || 0 ≤ u ≤ 1)
        return true
    end

    if case == 2
        return false
    end

    if case == 3 && (0 ≤ t ≤ 1 && 0 ≤ u ≤ 1)
        return true
    end

    if case == 4
        return false
    end

    return false
end

function segment_block_intersection(segment, block)
    return any((
        segment_segment_intersection(segment, block.s1),
        segment_segment_intersection(segment, block.s2),
        segment_segment_intersection(segment, block.s3),
        segment_segment_intersection(segment, block.s4),
    ))
end

function temple_segment_intersection(temple, segment)
    return any(segment_block_intersection(segment, block) for block ∈ temple.blocks)
end

function temple_ray_intersection(temple, ray)
    t_min = ∞
    for block ∈ temple.blocks
        for segment ∈ [block.s1, block.s2, block.s3, block.s4]
            (case, t, u) = ray_segment_intersection(ray, segment)
            if (case == 2 || case == 3) && (t < t_min) && (t > ε)
                t_min = t
            end
        end
    end

    return t_min
end

function check_solution(temple, lamp, mirrors)
    # check the lamp is within the temple
    if !all([0, 0] .≤ lamp.v .≤ temple.size)
        println(stderr, "ERROR! The lamp isn't placed within temple limits which is of size $(temple.size).")
        finalize(temple, lamp, mirrors)
    end

    # check mirrors' ends are within the temple
    if !all(all([0, 0] .≤ mirror.v1 .≤ temple.size) for mirror ∈ mirrors)
        println(stderr, "ERROR! Some mirror isn't placed within temple of size $(temple.size).")
        finalize(temple, lamp, mirrors)
    end

    if !all(all([0, 0] .≤ mirror.v2 .≤ temple.size) for mirror ∈ mirrors)
        println(stderr, "ERROR! Some mirror isn't placed within temple of size $(temple.size).")
        finalize(temple, lamp, mirrors)
    end
    
    # check the lamp isn't in some building block
    if point_in_block(temple, lamp.v)
        println(stderr, "ERROR! Lamp is placed in a building block.")
        finalize(temple, lamp, mirrors)
    end
    
    # check some mirror end isn't in some building block
    for (m, mirror) ∈ enumerate(mirrors)
        if point_in_block(temple, mirror.v1) || point_in_block(temple, mirror.v2)
            println(stderr, "ERROR! Mirror $m has one of its ends inside a building block.")
            finalize(temple, lamp, mirrors)
        end
    end

    # check some mirror doesn't overlap with some building block
    for (m, mirror) ∈ enumerate(mirrors)
        if temple_segment_intersection(temple, mirror.s)
            println(stderr, "ERROR! Mirror $m intersects with a building block.")
            finalize(temple, lamp, mirrors)
        end
    end
    
    # check if some mirrors intersect
    for (m1, mirror1) ∈ enumerate(mirrors[1:end-1]), (m2, mirror2) ∈ enumerate(mirrors[m1+1:end])
        if segment_segment_intersection(mirror1.s, mirror2.s)
            println(stderr, "ERROR! Mirrors $m1 & $(m1 + m2) intersect.")
            finalize(temple, lamp, mirrors)
        end
    end
    
    println(stderr, "The solution geometry is correct.")
end

function raytrace(temple, lamp, mirrors)
    local hit_mirror

    path = (
        points=[lamp.v],
        directions=[],
    )

    ray = (
        v = lamp.v,
        e = lamp.e
    )

    hit_mirrors = []
    while true
        # check if ray can hit some mirror
        t_mirror = ∞
        for (m, mirror) ∈ enumerate(mirrors)
            (case, t, u) = ray_segment_intersection(ray, mirror.s)
            if ((case == 2) || (case == 3)) && (t < t_mirror) && (t > ε)
                t_mirror = t
                hit_mirror = mirror
                push!(hit_mirrors, m)
            end
        end

        # check where ray would hit the temple
        t_temple = temple_ray_intersection(temple, ray)

        # closest hit point
        t = min(t_mirror, t_temple)
        hitting_point = ray.v + t * ray.e
        push!(path.directions, ray.e)
        push!(path.points, hitting_point)

        # ray hit a mirror, calculate new direction
        if t_mirror < t_temple
            ray = (
                v = hitting_point,
                e = ray.e - 2 * (ray.e ⋅ hit_mirror.n) * hit_mirror.n
            )
            continue
        end

        # ray hit the temple
        break
    end

    return path
end

function cmc24_plot(temple; lamp=nothing, mirrors=nothing, path=nothing)
    plot_scale = 150
    plot_size = plot_scale .* temple.shape 
    
    plot(
        size = plot_size,
        xlims = (0, temple.size[1]),
        ylims = (0, temple.size[2]),
        background_color = RGBA(0.9, 0.87, 0.7, 1),
        label = false,
        showaxis = false,
        grid = false,
        legend = false,
        aspect_ratio = 1,
        bottom_margin = -20mm,
        right_margin = -10mm,
        top_margin = -10mm,
        left_margin = -20mm,
    )
    
    function circleShape(x, y, r, n)
        θ = LinRange(0, 2π, n+1)
        return Shape(x .+ r*cos.(θ), y .+ r*sin.(θ))
    end
    
    # plot the lightened area
    if path ≠ nothing
        # circle parts of the lightened area
        for p ∈ path.points
            plot!(
                circleShape(p[1], p[2], light_halfwidth, 1000),
                color = RGBA(1, 0.7, 0.6, 1),
                linecolor = RGBA(0, 0, 0, 0),
                linewidth = 0,
            )    
        end
        
        # rectangle parts of the lightened area
        for (p1, p2, e) ∈ zip(path.points, path.points[2:end], path.directions)
            (x1, y1) = p1
            (x2, y2) = p2
            (nx, ny) = (e[2], -e[1])
            
            xs = [x1 - nx, x2 - nx, x2 + nx, x1 + nx]
            ys = [y1 - ny, y2 - ny, y2 + ny, y1 + ny]
            
            plot!(
                Shape(xs, ys),
                color = RGBA(1, 0.7, 0.6, 1),
                linecolor = RGBA(0, 0, 0, 0),
                linewidth = 0,
            )    
        end
    end
    
    # plot the mirrors
    if mirrors ≠ nothing
        for mirror ∈ mirrors
            (x1, y1) = mirror.v1
            (x2, y2) = mirror.v2
            (nx, ny) = 0.05 * mirror.n

            xs = [x1 - nx, x2 - nx, x2 + nx, x1 + nx]
            ys = [y1 - ny, y2 - ny, y2 + ny, y1 + ny]

            plot!(
                Shape(xs, ys),
                color = RGBA(0, 0, 1, 1),
                linecolor = RGBA(0, 0, 0, 0),
                linewidth = 0,
            )    
        end
    end

    # plot the ray
    if path ≠ nothing
        plot!(
            first.(path.points),
            last.(path.points),
            linecolor = RGBA(1, 0, 0, 1),
            linewidth = 0.04 * plot_scale,
        )
    end

    # plot the lamp
    if lamp ≠ nothing
        plot!(
            circleShape(lamp.v[1], lamp.v[2], 0.2, 6),
            color = RGBA(0.9, 0, 1, 1),
            linecolor = RGBA(1, 1, 1, 1),
            linewidth = 5,
        )    
    end
    
    # plot the building blocks
    for block ∈ temple.blocks
        (x, y) = block.v1
        plot!(
            Shape(
                x .+ [0, block_size, block_size, 0],
                y .+ [0, 0, block_size, block_size]),
            color = RGBA(0.50, 0.48, 0.47, 1),
            linecolor = RGBA(0, 0, 0, 0),
            linewidth = 0,
        )
    end
    
    solution_hash = hex12(hash([temple, lamp, mirrors, path]))
    uuid = hex12(UUIDs.uuid4().value)
    filename = "cmc24_solution_" * solution_hash * "_" * uuid * ".png"
    savefig(filename)
    
    return filename
end

function evaluate(temple, path)
    fplot1 = cmc24_plot(temple)
    fplot2 = cmc24_plot(temple, path=path)
    
    img1 = FileIO.load(fplot1)
    img2 = FileIO.load(fplot2)
    
    # count the total number of the plot pixels
    total = length(img1)
    
    # count the number of vacant pixels recognized by being bright
    vacant = sum(p.r > 0.7 for p ∈ img1)
    
    # count the number of pixels changed due to the light ray
    score = sum(p1 ≠ p2 for (p1, p2) ∈ zip(img1, img2))
    
    return total, vacant, score
end

function finalize(temple=nothing, lamp=nothing, mirrors=nothing, path=nothing)
    if temple ≠ nothing
        cmc24_plot(temple, lamp=lamp, mirrors=mirrors, path=path)
    end
    
    print(0)  # stdout print of a fallback result in a case of early exit

    exit()
end

# cmc24_solution = [
#     5 5 0.26;
#     11.5 6.5 0.9;
#     11.9 16.5 0.95;
#     15.2 17.6 2.45;
#     13.8 12.0 0.92;
#     1.6 6.2 2.53;
#     2.2 14.7 0.66;
#     18 12 1.6;
#     13.8 11.5 -0.54;
# ]

# cmc24_solution = [
#     5 5 0.26;
#     11.5 6.5 0.9;
#     11.9 16.5 0.95;
#     15.2 17.6 2.45;
#     13.8 12.0 0.92;
#     1.6 6.2 2.53;
#     2.2 14.7 0.7;
#     8.5 14.2 2.325;
#     8.7 3.05 2.525;
# ]

cmc24_solution = [
    13.960031014352973 12.692941424140095 3.141278494324434;
13.211994171142578 12.486725807189941 0.8854473829269409;
13.819404602050781 11.879109382629395 2.979506254196167;
17.785497665405273 18.468313217163086 2.9345970153808594;
18.5325984954834 7.048974514007568 1.426902413368225;
16.405689239501953 1.1330127716064453 3.1412785053253174;
12.020002365112305 10.905294418334961 2.699475049972534;
8.512105941772461 9.990828514099121 2.841191291809082;
4.804252624511719 14.770608901977539 3.0825445652008057
]

# cmc24_solution = [
#     5 5 0;
#     1 1 0;
#     11.9 16.5 0.95;
#     15.2 17.6 2.45;
#     13.8 12.0 0.92;
#     1.6 6.2 2.53;
#     2.2 14.7 0.66;
#     18 12 1.6;
#     13.8 11.5 -0.54;
# ]

# load the temple
temple = load_temple(temple_string, block_size)

# load the solution
lamp, mirrors = load_solution(cmc24_solution, mirror_length)
check_solution(temple, lamp, mirrors)

# compute the ray path
path = raytrace(temple, lamp, mirrors)

# evaluate the solution
total, vacant, score = evaluate(temple, path)
println(stderr, "Base plot has $(commas(vacant)) vacant of total $(commas(total)) pixels.")
println(stderr, "Your CMC24 score is $(commas(score)) / $(commas(vacant)) = $(100. * score / vacant) %.")
print(score)

# create the presentation plot
cmc24_plot(temple, lamp=lamp, mirrors=mirrors, path=path)
