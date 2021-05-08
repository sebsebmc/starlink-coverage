# Developing
This pile of scripts grew pretty organically as I was testing and messing around. As a result there are a lot of extra dependencies and very poor
organization of a lot of the code. If you want to generate the data yourself I will try and explain what is necessary here.

## Dependencies
You need a few deps today:
```
apt install -y parallel libgeos-c1v5 libgeos-3.8.0 libgeos-dev proj-data proj-bin libproj15 libproj-dev
```

## Running

```
make install-deps
make generate-coverage
```

### Python
These are the minimal dependencies, any code that uses cartopy can be removed ignored if you're not debugging like I was
 - Skyfield
 - h3
 - numpy
 - geog

### Javascript
I am not using any installed dependencies in my environment, all the dependencies are hosted by CDNs. They are:
 - CesiumJS
 - h3-js
 - ChromaJS

### Shell
I use GNU parallel to make running the script across 4 cores easier. As promised here is the citation:

    Tange (2011): GNU Parallel - The Command-Line Power Tool,
    ;login: The USENIX Magazine, February 2011:42-47.
