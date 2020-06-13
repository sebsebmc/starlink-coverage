# Goals:

1. % of day covered
2. Average coverage (factoring the number of satellites covering a location)

## Implementation

1. TLE to ground track
2. Altitude,x,y to conical section on sphere
   a. Adjustable minimum elevation
   b. Swap out for more accurate model of earth (WGS-84 ellipsoid)
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
2048*1024 = 2,097,152
4096*2048 = 8,388,608‬

Instead of trying to use a 2d array to represent the footprints and dealing with the spherical nature
of the Earth, I am instead going to try and use S2 level 9 cells to track coverage. According to the
statistics page of the S2 library, this is about 1537000 cells, so I would need about 12MB of data to
track the whole Earth. Each cell covers 324.29km^2 on average.

For temporal resolution:
These satellites move across a location quite quickly, using a website like https://findstarlink.com
we can find that a whole "train" of Starlink satellites crosses a locations view in about 4 or 5 minutes
so our temporal resolution needs to be a minute if not faster if we want accurate results. 

## S2 based approach

```
for each time step:
    for each sat:
        calculate footprint
        get cells to cover footprint
        for each cell:
            increment counter
```

This means we only have to iterate over ~2200 cells per satellite instead of ~2 million points each.

## Used constants

- Earth Mean Equitorial Radius = 6,378.1km
- Minimum angle for user terminals = 35deg
-

## Starlink details

From the second reference below I found that Starlink is targeting user terminal minimum angles of 35deg
This means that each satellite covers around 600,000km^2 at an altitude of about 340km. However, most of
the starlink satellites already in space are elevating or are at 550 km

Stralink TLE's
https://celestrak.com/NORAD/elements/starlink.txt


### References

https://arxiv.org/pdf/1906.12318.pdf
https://licensing.fcc.gov/myibfs/download.do?attachment_key=1190019
