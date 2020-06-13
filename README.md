# Goals:

1. % of day covered
2. Average coverage (satellite multiplicity)

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

2 options:
2048*1024 = 2,097,152
4096*2048 = 8,388,608‬

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

## Remaining questions

Does

### References

https://arxiv.org/pdf/1906.12318.pdf
https://licensing.fcc.gov/myibfs/download.do?attachment_key=1190019
