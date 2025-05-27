# Welcome to Monty Extension Documentation

## About Monty

Monty, an abbreviated name for the Montandon - Global Crisis Data Bank, is a database that brings in hazard and impact data for current, historical and forecasted disasters around the globe. By combining lots of different sources of information, Monty aims to fill-in-the-gaps and provide a more complete picture of disaster risk for the National Societies.

<div class="video-wrapper">
  <iframe
    src="https://www.youtube.com/embed/BEWxqYfrQek"
    title="Montandon Project Overview"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    allowfullscreen
  ></iframe>
</div>

## Overview

This specification explains the Montandon Extension to the [SpatioTemporal Asset Catalog](https://github.com/radiantearth/stac-spec) (STAC) specification. It provides a way to include Montandon data from [Montandon model analysis](model/README.md) in a STAC Item or Collection.

## Getting Started

1. First, understand the [model](model/README.md) and its components
2. Review the [example collections](examples/index.md) for practical implementations
3. Explore available [data sources](model/sources/README.md)

## Documentation Sections

- **Model**: Core documentation about the Monty data model
- **Examples**: Example collections and their usage in validation
- **Sources**: Details about each data source and integration

<style>
.video-wrapper {
    position: relative;
    padding-bottom: 56.25%; /* 16:9 aspect ratio */
    height: 0;
    margin: 20px 0;
}

.video-wrapper iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}
</style>
