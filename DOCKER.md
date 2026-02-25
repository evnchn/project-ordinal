# Docker Guide for Project Ordinal

## What the App Does

Project Ordinal is a NiceGUI web application for HKUST students to look up their GPA rank and exam score percentiles. It provides the following pages:

- **`/`** -- SENG Year 1 GPA rank lookup (Fall 2022 cohort, 720-based GPA fractions)
- **`/math1014mt`** -- MATH1014 Midterm score percentage lookup (linear and cubic interpolation)
- **`/math1014fn`** -- MATH1014 Final score percentage lookup (linear and cubic interpolation)
- **`/comp2012hmt`** -- COMP2012H Midterm score percentage lookup (linear and cubic interpolation)

## Building the Docker Image

```bash
docker build -t project-ordinal .
```

## Running the Container

```bash
docker run -p 8080:8080 project-ordinal
```

Then open your browser at [http://localhost:8080](http://localhost:8080).

To run in detached (background) mode:

```bash
docker run -d -p 8080:8080 project-ordinal
```

To map to a different host port (e.g. 3000):

```bash
docker run -p 3000:8080 project-ordinal
```

## Environment Variables

This application does not use any environment variables. All data is loaded from JSON files bundled in the image.

## Port Mapping

The NiceGUI application listens on port **8080** inside the container. Map it to any host port using the `-p` flag:

```
-p <host_port>:8080
```
