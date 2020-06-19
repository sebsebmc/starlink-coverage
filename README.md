# Goals:

1. % of day covered
2. Average coverage - factoring the number of satellites covering a location which would be more useful for approximating average bandwith available for an area

## Original Implementation

1. TLE to simulate satellites
2. Altitude,x,y to conical section on sphere
    1. Adjustable minimum elevation
    2. Swap out for more accurate model of earth (WGS-84 ellipsoid)
3. Map conical section to equi-rectangular area
4. Translate to pixel coords with resolution of about 100sq mi
5. Normalize? Overlay

For the core there is this naive implementation:

```
for each time step:
    for each pixel:
        convert to lat/long
        for each sat:
            if visible
                increase counter for pixel
```

This seems like a pretty gross way to do it. We touch every pixel \* numSats, when we could reduce to
numSats \* visible area. However, the math to calculate visible area for a satellite doesn't seem to
be a part of any library I've found. This is even more relevant with VLEO satellites since they cover
so much less area. I'm not sure how efficient it is to go from sphere to lat/long
on an equi-rectangular projection.

## Resolution

2 options for spatial resolution in my head originally:
- 2048 x 1024 = 2,097,152
- 4096 x 2048 = 8,388,608‬

Instead of trying to use a 2d array to represent the footprints and dealing with the spherical nature
of the Earth, I am instead going to try and use S2 level 9 cells to track coverage. According to the
statistics page of the S2 library, this is about 1537000 cells, so I would need about 12MB of data to
track the whole Earth. Each cell covers 324.29km^2 on average.

For temporal resolution:
These satellites move across a location quite quickly, using a website like https://findstarlink.com
we can find that a whole "train" of Starlink satellites crosses a locations view in about 4 or 5 minutes
so our temporal resolution needs to be a minute if not faster if we want accurate results. 

## S2 based approach
The original implementation has lots of gross properties and requires dealing with many projections.
So I tried using a new approach that used ~ equal area tesselated grids. The one I knew about was S2 so I tried that first.
```
for each time step:
    for each sat:
        calculate footprint
        get cells to cover footprint
        for each cell:
            increment counter
```

This means we only have to iterate over ~2000 (+/-600?) cells per satellite instead of ~2 million 
points each. However, this approach seems too slow. Comptuing all the covering cells of each satellite
takes about 90s on a single core in Python. While this could be parallelized, I think maybe there
are even smarter approaches to consider. Could we maybe just store S2Cap objects and test points
against them to count the amount of coverage? What I really like from S2 is that it handles the
issues of latitude and longitude meaning different distances at the equator vs the poles.

In the end for plotting, if we used the cell vertices as plotting locations we would cover the whole
globe and not oversample at the poles or undersample at the equator.

## S2, more like 2Slow... An H3 approach
So S2 was just being way to slow to return cells for a given covering. (90s to simulate one timestep)
Now I have to make some guesses about projections for H3 and but it is ~4.5 times faster to simulate 
a timestep than S2 (now takes 20 seconds on my machine). I'm gonna proceed with the H3 approach for
now.

## Used constants

- Earth Mean Equitorial Radius = 6,378.1km
- Minimum angle for user terminals = 35deg

(It has recently come to my attention that there may be newer data from SpaceX that the minimum user terminal angle would be 25 degrees, so my data may be more conservative. The data I used is from the FCC document linked below.)

## Starlink details

From the second reference below I found that Starlink is targeting user terminal minimum angles of 35deg
This means that each satellite covers around 600,000km^2 at an altitude of about 340km. However, most of
the starlink satellites already in space are elevating or are at 550 km

Stralink TLE's
https://celestrak.com/NORAD/elements/starlink.txt

## Issues at the IDL (anitmeridian)?
When visualizing the data we see that there is less coverage at the international date line. This doesn't
really make a lot of sense given the surrounding areas and the orbits the satellites are in. To me this
means there is an issue in the math, namely the calculations for the cap sphere are likely going beyond
180 and -180 degrees, but GeoJSON seems to handle these coordinates just fine. Turns out its an issue 
with H3 https://github.com/uber/h3/issues/210 that seems like a pain to deal with.

### References

- https://arxiv.org/pdf/1906.12318.pdf
- https://licensing.fcc.gov/myibfs/download.do?attachment_key=1190019
