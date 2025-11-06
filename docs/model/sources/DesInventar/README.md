# Desinventar

[Desinventar](https://www.desinventar.net/) is a conceptual and methodological tool for generating national disaster databases that provides access to disaster effects information at various scales. It is maintained by the United Nations Office for Disaster Risk Reduction (UNDRR).

## Collection: `desinventar-events`

A STAC collection holds all Desinventar events. The example collection is at `examples/desinventar-events/desinventar-events.json`.

- Name: Desinventar Event Data
- Code: `Desinventar`
- Source organisation: United Nations Office for Disaster Risk Reduction (UNDRR)
- Source code: UNDRR
- Source Type: International Organization
- Source organization email: <desinventar@un.org> 
- Source URL: <https://www.desinventar.net>
- Source Data license: [License](https://www.desinventar.net/terms_of_use.html)
- Source for: event, hazard, impact

### Data

Desinventar data is available as downloadable ZIP files containing:

- An XML file with event data (DI_export_{country_code}.xml)
- Shapefiles for administrative boundaries
- Additional metadata files

#### API Endpoints

- Base URL: `https://www.desinventar.net`
- Export endpoint: `https://www.desinventar.net/DesInventar/download/DI_export_{country_code}.zip`

The country code must be provided in lowercase (e.g., 'npl' for Nepal).

The zip archive contains the following files:

- DI_export_{country_code}.xml: Event data in Desinventar XML format
- district.shp/dbf/prj/shx: Shapefiles for disctrict administrative boundaries
- region.shp/dbf/prj/shx: Shapefiles for region administrative boundaries
- village.shp/dbf/prj/shx: Shapefiles for village administrative boundaries

##### XML Data

The XML file is structured as follows:

```xml
<DESINVENTAR>
    <datamodel>
        <!-- Data model definition -->
    </datamodel>
    <eventos>
        <!-- Event type list -->
    </eventos>
    <causas>
        <!-- Hazard type (Cause) list -->
    </causas>
    <niveles>
        <!-- Administrative level list -->
    </niveles>
    <lev0>
        <!-- Top-level administrative names list -->
    </lev0>
    <lev1>
        <!-- First-level administrative names list -->
    </lev1>
    <lev2>
        <!-- Second-level administrative names list -->
    </lev2>
    <regiones>
        <!-- Administrative boundaries (bounding boxes) for each administrative name -->
    </regiones>
    <diccionario>
        <!-- Taxonomy of impact categories -->
    </diccionario>
    <fichas>
        <!-- Event data -->
    </fichas>
    <level_maps>
        <!-- Shapefile listing -->
    </level_maps>
</DESINVENTAR>

Each disaster event is stored as a `<TR>` element within the `<fichas>` section:

```xml
<fichas>
    <TR>
        <serial>194</serial>
        <level0>GRD</level0>              <!-- Country code -->
        <level1>GRD01</level1>            <!-- Region code -->
        <level2>GRD01001</level2>         <!-- District code -->
        <name0>Grenada</name0>            <!-- Country name -->
        <name1>Saint George</name1>       <!-- Region name -->
        <name2>Saint George City</name2>  <!-- District name -->
        <evento>STORM</evento>            <!-- Hazard type -->
        <lugar>National - TS Ernesto</lugar> <!-- Location description -->
        
        <!-- Temporal information -->
        <fechano>2012</fechano>
        <fechames>8</fechames>
        <fechadia>3</fechadia>
        <duracion>0</duracion>            <!-- Duration in days -->
        
        <!-- Impact metrics -->
        <muertos>0</muertos>              <!-- Deaths -->
        <heridos>0</heridos>              <!-- Injured -->
        <desaparece>0</desaparece>        <!-- Missing -->
        <damnificados>0</damnificados>    <!-- Directly affected -->
        <afectados>0</afectados>          <!-- Indirectly affected -->
        <vivdest>0</vivdest>              <!-- Houses destroyed -->
        <vivafec>0</vivafec>              <!-- Houses damaged -->
        <evacuados>0</evacuados>          <!-- Evacuated -->
        <reubicados>0</reubicados>        <!-- Relocated -->
        <valorus>0</valorus>              <!-- Losses in USD -->
        <valorloc>0</valorloc>            <!-- Losses in local currency -->
        <nhectareas>0</nhectareas>        <!-- Crop area damaged (ha) -->
        <cabezas>0</cabezas>              <!-- Cattle lost -->
        <kmvias>0</kmvias>                <!-- Roads damaged (m) -->
        
        <!-- Additional information -->
        <magnitud2></magnitud2>           <!-- Hazard magnitude -->
        <glide></glide>                   <!-- GLIDE number if available -->
        <latitude>0</latitude>
        <longitude>0</longitude>
    </TR>
</fichas>
```

### Event Item

A Desinventar event will **ALWAYS** produce an [**event STAC item**](https://github.com/IFRCGo/monty-stac-extension#event).

Example event items for grenada export at [DI_export_GRD.xml](DI_export_grd.xml):

- [STORM grd-194.json](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/desinventar-events/grd-194.json)
- [EPIDEMIC grd-200.json](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/desinventar-events/grd-200.json)

Here is the mapping of fields from Desinventar XML to STAC event items:

| STAC field                                                                                                         | Desinventar field                                  | Description                                                                             |
| ------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------- | --------------------------------------------------------------------------------------- |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)                              | level0 (lower case) + '-' + serial                 | Unique identifier combining country code and event serial                               |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)                  | Based on shapefile data using level2/level1/level0 | Geometry derived from administrative boundaries                                         |
| [bbox](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#bbox)                          | Calculated from geometry                           | Bounding box of the event area                                                          |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#datetime)                  | fechano, fechames, fechadia                        | Date of the event                                                                       |
| [start_datetime](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#date-and-time) | fechano, fechames, fechadia                        | Start date of the event                                                                 |
| [end_datetime](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#date-and-time)   | fechano, fechames, fechadia + [duracion]           | End date of the event                                                                   |
| [title](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#item-properties)        | evento + lugar + date                              | Human-readable title combining event type and location                                  |
| [monty:episode_number](https://ifrcgo.org/monty-stac-extension/v1.1.0/schema.json#monty:episode_number)                     | 1                                                  | Set to 1 as Desinventar doesn't track episodes                                          |
| [monty:country_codes](https://ifrcgo.org/monty-stac-extension/v1.1.0/schema.json#monty:country_codes)                       | level0                                             | ISO3 code of the event country                                                          |
| [monty:hazard_codes](https://ifrcgo.org/monty-stac-extension/v1.1.0/schema.json#monty:hazard_codes)                         | [mapped from evento](#hazard-code-mapping)         | Hazard codes mapped from Desinventar event types (see mapping below)                    |
| [monty:corr_id](https://ifrcgo.org/monty-stac-extension/v1.1.0/schema.json#monty:corr_id)                                   | Generated                                          | Generated following the [event correlation](../../correlation_identifier.md) convention |

#### Hazard Code Mapping

DesInventar uses its own hazard classification and must follow the **2025 UNDRR-ISC** code as the **reference classification** for the Monty extension. The following table provides cross-classification across multiple systems:

| DesInventar Event | GLIDE | EM-DAT              | **UNDRR-ISC 2025** (Reference) | Cluster    | Description                     |
| ----------------- | ----- | ------------------- | ------------------------------ | ---------- | ------------------------------- |
| ALLUVION          | MS    | nat-hyd-mmw-mud     | **GH0303**                     | GEO-GFAIL  | Flows (includes mudflow)        |
| AVALANCHE         | AV    | nat-geo-mmd-ava     | **MH0801**                     | MH-TERR    | Avalanche                       |
| COASTAL EROSION   | OT    | nat-geo-env-coa     | **GH0405**                     | GEO-OTHER  | Coastal Erosion & Accretion     |
| COLD WAVE         | CW    | nat-met-ext-col     | **MH0502**                     | MH-TEMP    | Cold Wave                       |
| CYCLONE           | TC    | nat-met-sto-tro     | **MH0306**                     | MH-WIND    | Cyclone or Depression           |
| DROUGHT           | DR    | nat-cli-dro-dro     | **MH0401**                     | MH-PRECIP  | Drought                         |
| EARTHQUAKE        | EQ    | nat-geo-ear-gro     | **GH0101**                     | GEO-SEIS   | Earthquake                      |
| ELECTRIC STORM    | ST    | nat-met-sto-lig     | **MH0102**                     | MH-CONV    | Lightning (electrical storm)    |
| EROSION           | OT    | nat-geo-env-soi     | **GH0403**                     | GEO-OTHER  | Soil Erosion                    |
| FLASH FLOOD       | FF    | nat-hyd-flo-fla     | **MH0603**                     | MH-WATER   | Flash Flooding                  |
| FLOOD             | FL    | nat-hyd-flo-flo     | **MH0600**                     | MH-WATER   | Flooding (chapeau)              |
| FOG               | OT    | nat-met-fog-fog     | **MH0202**                     | MH-PART    | Fog                             |
| FOREST FIRE       | WF    | nat-cli-wil-for     | **EN0205**                     | ENV-FOREST | Wildfires                       |
| FROST             | OT    | nat-met-ext-sev     | **MH0505**                     | MH-TEMP    | Frost (Hoar Frost)              |
| HAIL STORM        | ST    | nat-met-sto-hai     | **MH0404**                     | MH-PRECIP  | Hail                            |
| HEAT WAVE         | HT    | nat-met-ext-hea     | **MH0501**                     | MH-TEMP    | Heatwave                        |
| LAHAR             | VO    | nat-geo-vol-lah     | **GH0204**                     | GEO-VOLC   | Lahars                          |
| LANDSLIDE         | LS    | nat-geo-mmd-lan     | **GH0300**                     | GEO-GFAIL  | Gravitational Mass Movement     |
| LIQUEFACTION      | EQ    | nat-geo-ear-gro     | **GH0307**                     | GEO-GFAIL  | Liquefaction                    |
| SANDSTORM         | VW    | nat-met-sto-san     | **MH0201**                     | MH-PART    | Dust Storm or Sandstorm         |
| SNOW STORM        | OT    | nat-met-sto-bli     | **MH0406**                     | MH-PRECIP  | Snow Storm                      |
| STORM SURGE       | SS    | nat-met-sto-sur     | **MH0703**                     | MH-MARINE  | Storm Surge                     |
| TSUNAMI           | TS    | nat-geo-ear-tsu     | **MH0705**                     | MH-MARINE  | Tsunami                         |
| TORNADO           | TO    | nat-met-sto-tor     | **MH0305**                     | MH-WIND    | Tornado                         |

> [!NOTE]
> All three classification codes (GLIDE, EM-DAT, UNDRR-ISC 2025) should be included in the `monty:hazard_codes` array for maximum interoperability. More specific [hazard codes](../../taxonomy.md#complete-2025-hazard-list) can be added following the characteristics of the event.

This mapping enables standardized hazard categorization while preserving DesInventar's original classification in the source properties.

### Hazard Item

No hazard items are generated from Desinventar data as the hazard information is almost never available (`magnitud2` field is empty) and when available, it is hardly standardized.

### Impact Item

Desinventar events will produce multiple [**impact STAC items**](https://github.com/IFRCGo/monty-stac-extension#impact) when impact data is available.

Example impact items:

- [EPIDEMIC deaths grd-200-deaths.json](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/desinventar-impacts/grd-200-deaths.json)

The following table shows the mapping of Desinventar impact fields to STAC items:

| Desinventar field     | Category               | Type                | Unit    | Description                       |
| --------------------- | ---------------------- | ------------------- | ------- | --------------------------------- |
| deaths                | ALL_PEOPLE             | DEATHS              | count   | Number of deaths                  |
| injured               | ALL_PEOPLE             | INJURED             | count   | Number of injured people          |
| missing               | ALL_PEOPLE             | MISSING             | count   | Number of missing people          |
| houses_destroyed      | BUILDINGS              | DESTROYED           | count   | Houses completely destroyed       |
| houses_damaged        | BUILDINGS              | DAMAGED             | count   | Houses partially damaged          |
| directly_affected     | ALL_PEOPLE             | DIRECTLY_AFFECTED   | count   | People directly affected          |
| indirectly_affected   | ALL_PEOPLE             | INDIRECTLY_AFFECTED | count   | People indirectly affected        |
| relocated             | ALL_PEOPLE             | RELOCATED           | count   | People relocated                  |
| evacuated             | ALL_PEOPLE             | EVACUATED           | count   | People evacuated                  |
| losses_in_dollar      | TOTAL_COST_UNSPECIFIED | LOSS_COST           | USD     | Economic losses in USD            |
| losses_local_currency | TOTAL_COST_UNSPECIFIED | LOSS_COST           | Unknown | Economic losses in local currency |
| damages_in_crops_ha   | CROP                   | DAMAGED             | hectare | Crop area damaged                 |
| lost_cattle           | CATTLE                 | MISSING             | count   | Number of cattle lost             |
| damages_in_roads_mts  | ALL_PEOPLE             | DAMAGED             | m       | Length of roads damaged           |

For each available impact metric in the Desinventar data, a separate impact item is created with:

| STAC field                                                                                                  | Value                      | Description                                        |
| ----------------------------------------------------------------------------------------------------------- | -------------------------- | -------------------------------------------------- |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)                       | {level0}-{serial}-{metric} | Unique ID combining event serial and impact metric |
| [title](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#item-properties) | {event title} - {metric}   | Title combining event name and impact type         |
| [monty:impact_detail](https://ifrcgo.org/monty-stac-extension/v1.1.0/schema.json#monty:impact_detail)                |                            | Object containing impact details                   |
| monty:impact_detail.category                                                                                | From mapping table         | Impact category code                               |
| monty:impact_detail.type                                                                                    | From mapping table         | Impact type code                                   |
| monty:impact_detail.value                                                                                   | From Desinventar field     | Numeric impact value                               |
| monty:impact_detail.unit                                                                                    | From mapping table         | Unit of measurement                                |
| monty:impact_detail.estimate_type                                                                           | "primary"                  | All Desinventar data is considered primary         |

The geometry, bbox, datetime and other base fields are inherited from the source event item.
