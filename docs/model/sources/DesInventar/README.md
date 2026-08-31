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
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)                  | Based on shapefile data using level2/level1/level0 | Geometry derived from administrative boundaries (when admin level info is missing, get the geometry from iso3 using Geocoding service) |
| [bbox](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#bbox)                          | Calculated from geometry                           | Bounding box of the event area                                                          |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#datetime)                  | fechano, fechames, fechadia                        | Date of the event                                                                       |
| [start_datetime](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#date-and-time) | fechano, fechames, fechadia                        | Start date of the event                                                                 |
| [end_datetime](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#date-and-time)   | fechano, fechames, fechadia + [duracion]           | End date of the event                                                                   |
| [title](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#item-properties)        | evento + lugar + date                              | Human-readable title combining event type and location                                  |
| [monty:episode_number](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:episode_number)                     | 1                                                  | Set to 1 as Desinventar doesn't track episodes                                          |
| [monty:country_codes](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:country_codes)                       | level0                                             | ISO3 code of the event country                                                          |
| [monty:hazard_codes](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:hazard_codes)                         | [mapped from evento](#hazard-code-mapping)         | Hazard codes mapped from Desinventar event types (see mapping below)                    |
| [monty:corr_id](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:corr_id)                                   | Generated                                          | Generated following the [event correlation](../../correlation_identifier.md) convention |
| [monty:src_event_id](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:src_event_id) | Source event ID | |

#### Hazard Code Mapping

DesInventar uses its own hazard classification and must follow the **2025 UNDRR-ISC** code as the **reference classification** for the Monty extension. Raw `evento` values from the source are messy — typos, translations, capitalization variants, legacy codes — so the transformer resolves them in two steps (see [`desinventar.py`](https://github.com/IFRCGo/pystac-monty/blob/main/pystac_monty/sources/desinventar.py)):

1. **Normalization** — the raw `evento` value is looked up in a large alias table (`hazard_name_mappings`, 300+ entries) that collapses raw variants (e.g. `"HURRICANE"`, `"Typhoon"`, `"TC - Tropical Cyclone"`) down to one canonical event name (e.g. `CYCLONE`). If no alias matches, the raw value is used as-is.
2. **Code lookup** — the canonical event name is looked up in the `hazard_mapping` table below to get its `[UNDRR-ISC 2025, EM-DAT, GLIDE]` triplet.

> [!NOTE]
> If the canonical event name has no entry in `hazard_mapping`, or maps to `None`, the record is dropped — **no event item is produced** for it. See [Unmapped events](#unmapped-events) below.

The following table provides cross-classification across multiple systems, per [taxonomy.md](../../taxonomy.md) and [HazardProfiles.csv](https://github.com/IFRCGo/pystac-monty/blob/main/pystac_monty/HazardProfiles.csv):

| DesInventar Event | GLIDE | EM-DAT | **UNDRR-ISC 2025** (Reference) | Cluster | Description |
| ------------------ | ----- | ------------------- | ------------------------------- | ---------- | ------------------------------- |
| ACCIDENT | AC | tec-mis-col-col | **TL0007** † | TECH-STRFAIL | Structural Failure |
| Acid rain | OT |  | **EN0105** | ENV-AIR | Acid Rain |
| AFLATOXIN | OT |  | **CH0201** | CHEM-CARC | Aflatoxins |
| Air pollution | OT |  | **EN0102** | ENV-AIR | Air Pollution (Point Source) |
| AIRCRAFT CRASH | AC | tec-tra-air-air | **TL0401** | TECH-TRANSP | Air Transportation Accident |
| ALLUVION | MS | nat-hyd-mmw-mud | **GH0303** | GEO-GFAIL | Flows |
| ANIMAL ATTACK | OT |  | **BI0604** | BIO-OTHER | Human-Wildlife Conflict |
| ANIMAL DISEASE | OT |  | **BI0301** | BIO-ANIMAL | Animal Diseases (Not Zoonoses) |
| ASPHYXIA | OT |  | **CH0400** | CHEM-AGAS | Asphyxiant Gases |
| AVALANCHE | AV | nat-geo-mmd-ava | **MH0801** | MH-TERR | Avalanche |
| BOAT CAPSIZE | AC | tec-tra-wat-wat | **TL0050** † | TECH-TRANSP | Marine Accident |
| BREACH | FL | tec-mis-col-col | **TL0205** | TECH-STRFAIL | Dam Failure |
| CHEMICAL SUBSTANCE | OT |  | **CH0903** | CHEM-OTHER | Chemical Warfare Agents |
| Cholera | OT |  | **BI0204** | BIO-SPEC | Cholera (Human) |
| COASTAL EROSION | OT | nat-geo-env-sed | **GH0405** | GEO-OTHER | Coastal Erosion & Accretion |
| COASTAL FLOOD | FL | nat-hyd-flo-coa | **MH0601** | MH-WATER | Coastal Flooding |
| COLD WAVE | CW | nat-met-ext-col | **MH0502** | MH-TEMP | Cold Wave |
| CONFLICT | CE |  | **SO0103** | SOC-CONF | Civil Unrest |
| CONTAMINATION | OT |  | **EN0103** | ENV-AIR | Ambient (Outdoor) Air Pollution |
| CYCLONE | TC | nat-met-sto-tro | **MH0309** | MH-WIND | Tropical Cyclone |
| Deforestación | OT |  | **EN0201** | ENV-FOREST | Deforestation |
| DOMESTIC FIRE | FR | tec-ind-fir-fir | **TL0305** | TECH-INDFAIL | Fire |
| DROUGHT | DR | nat-cli-dro-dro | **MH0401** | MH-PRECIP | Drought |
| DROWNING | AC | tec-tra-wat-wat | **TL0403** | TECH-TRANSP | Maritime Accident |
| DZUD | OT | nat-met-ext-sev | **MH0503** | MH-TEMP | Dzud |
| EARTHQUAKE | EQ | nat-geo-ear-gro | **GH0101** | GEO-SEIS | Earthquake |
| ELECTROCUTION | OT |  | **TL0209** | TECH-STRFAIL | Power Outage / Blackout |
| EPIDEMIC | EP ‡ | nat-bio-epi-dis | **BI0101** | BIO-INFECT | Airborne Diseases (human and Animal) |
| EPIZOOTIC |  | nat-bio-ani-ani | **BI0027** † | BIO_INFDISANIHUM | Zoonotic Diseases |
| EROSION | OT | nat-geo-env-soi | **GH0403** | GEO-OTHER | Soil Erosion |
| EXPLOSION | AC | tec-ind-exp-exp | **TL0029** † | TECH-INDFAIL | Explosion |
| EXPLOSIONS | AC | tec-ind-exp-exp | **TL0304** | TECH-INDFAIL | Explosion |
| FIRE | WF | nat-cli-wil-wil | **EN0205** | ENV-FOREST | Wildfires |
| FISSURES | EQ | nat-geo-ear-gro | **GH0311** | GEO-GFAIL | Surface Rupture & Fissure |
| FLASH FLOOD | FF | nat-hyd-flo-fla | **MH0603** | MH-WATER | Flash Flooding |
| FLOOD | FL | nat-hyd-flo-flo | **MH0600** | MH-WATER | Flooding |
| FOG | OT | nat-met-fog-fog | **MH0202** | MH-PART | Fog |
| FOREST FIRE | WF | nat-cli-wil-for | **EN0205** | ENV-FOREST | Wildfires |
| Freezing Rain | OT | nat-met-ext-sev | **MH0506** | MH-TEMP | Freezing Rain (Supercooled Rain) |
| FROST | OT | nat-met-ext-sev | **MH0505** | MH-TEMP | Frost (Hoar Frost) |
| GALE | OT |  | **MH0303** | MH-WIND | Gale |
| GAS SPILLS | AC | tec-ind-gas-gas | **TL0301** | TECH-INDFAIL | Leaks and Spills |
| GLACIAL LAKE OUTBURST FLOOD | FL | nat-cli-glo-glo | **MH0607** | MH-WATER | Glacial Lake Outburst Flooding |
| GUNSHOT | OT |  | **SO0301** | SOC-BEH | Violence |
| HAIL STORM | ST | nat-met-sto-hai | **MH0404** | MH-PRECIP | Hail |
| HEAT WAVE | HT | nat-met-ext-hea | **MH0501** | MH-TEMP | Heatwave |
| HEAVY RAINS | OT |  | **MH0402** | MH-PRECIP | Rain |
| Hundimiento | OT | nat-geo-mmd-sub | **GH0308** | GEO-GFAIL | Sinkhole |
| INTOXICACION | OT |  | **CH0601** | CHEM-FOOD | Levels of Contaminants in Food & Feed |
| LAHAR | VO | nat-geo-vol-lah | **GH0204** | GEO-VOLC | Lahars |
| LAND DEGRADATION | OT |  | **EN0301** | ENV-LAND | Land Degradation |
| LANDSLIDE | LS | nat-geo-mmd-lan | **GH0300** | GEO-GFAIL | Gravitational Mass Movement (Landslide) |
| LEAK | AC | tec-ind-che-che | **TL0030** † | TECH-INDFAIL | Leaks and Spills |
| LEAK OR SPILL | AC | tec-ind-che-che | **TL0301** | TECH-INDFAIL | Leaks and Spills |
| LIGHTNING | ST | nat-met-sto-lig | **MH0102** | MH-CONV | Lightning (electrical storm) |
| LIQUEFACTION | EQ | nat-geo-ear-gro | **GH0307** | GEO-GFAIL | Liquefaction |
| LOCUST CRISIS | IN | nat-bio-inf-loc | **BI0402** | BIO-INSECT | Locust |
| MALARIA | OT |  | **BI0219** | BIO-SPEC | Malaria (Human) |
| MEASLE | OT |  | **BI0221** | BIO-SPEC | Measles (Human) |
| MENINGITIS | OT |  | **BI0222** | BIO-SPEC | Meningococcal Meningitis (Human) |
| MINING HAZARD | OT |  | **TL0307** | TECH-INDFAIL | Mining Hazards |
| Mpox | OT |  | **BI0224** | BIO-SPEC | Mpox (Human) |
| Nuclear accidents | OT |  | **TL0208** | TECH-STRFAIL | Nuclear Plant Failure |
| PEST | IN | nat-bio-inf-loc | **BI0401** | BIO-INSECT | Insect Pest Infestations |
| PLAGUE | OT |  | **BI0228** | BIO-SPEC | Plague (Human) |
| POLLUTION | OT |  | **TL0302** | TECH-INDFAIL | Pollution |
| Racionamiento | OT |  | **TL0210** | TECH-STRFAIL | Water Supply Failure |
| RAIN | OT |  | **MH0402** | MH-PRECIP | Rain |
| RIVER FLOOD | FL | nat-hyd-flo-riv | **MH0604** | MH-WATER | Fluvial (Riverine) Flooding |
| RIVERBANK EROSION | OT |  | **GH0404** | GEO-OTHER | River Erosion & Accretion |
| ROAD ACCIDENT | AC | tec-tra-roa-roa | **TL0405** | TECH-TRANSP | Road Traffic Accident |
| ROCK FALL | OT |  | **GH0301** | GEO-GFAIL | Falls |
| SANDSTORM | VW | nat-met-sto-san | **MH0201** | MH-PART | Dust Storm or Sandstorm |
| SEA LEVEL RISE | OT |  | **EN0402** | ENV-WATER | Sea Level Rise |
| SNAKE BITE | OT |  | **BI0605** | BIO-OTHER | Snakebite Envenoming |
| SNOW STORM | OT |  | **MH0406** | MH-PRECIP | Snow Storm |
| Snowfall | OT |  | **MH0405** | MH-PRECIP | Snow |
| STORM | ST | nat-met-sto-sto | **MH0103** | MH-CONV | Thunderstorm |
| STRONG WIND | VW | nat-met-sto-sto | **MH0301** | MH-WIND | Wind |
| STRUCT.COLLAPSE | AC | tec-mis-col-col | **TL0005** † | TECH-STRFAIL | Building Collapse |
| STRUCTURE | AC | tec-mis-col-col | **TL0201** | TECH-STRFAIL | Building Collapse |
| SUBSIDENCE |  | nat-geo-ear-gro | **GH0309** | GEO-GFAIL | Subsidence and Uplift |
| SURGE | SS | nat-met-sto-sur | **MH0703** | MH-MARINE | Storm Surge |
| THUNDERSTORM | ST | nat-met-sto-sto | **MH0103** | MH-CONV | Thunderstorm |
| TIDAL WAVES | OT | nat-hyd-wav-rog | **MH0701** | MH-MARINE | Rogue Wave |
| TORNADO | TO | nat-met-sto-tor | **MH0305** | MH-WIND | Tornado |
| TRAIN CRASH | AC | tec-tra-rai-rai | **TL0404** | TECH-TRANSP | Rail Accident |
| TSUNAMI | TS | nat-geo-ear-tsu | **MH0705** | MH-MARINE | Tsunami |
| URBAN FLOOD | OT |  | **MH0606** | MH-WATER | Surface water Flooding |
| VOLCANO | VO | nat-geo-vol-vol | **GH0205** | GEO-VOLC | Volcanic Gases and Aerosols |
| WETLAND LOSS/DEGRADATION | OT |  | **EN0304** | ENV-LAND | Wetland Loss/Degradation |
| YELLOW FEVER | OT |  | **BI0241** | BIO-SPEC | Yellow Fever (Human) |

> † These six entries still carry pre-2025 UNDRR-ISC codes from the 2020 Hazard Information Profiles (historical reference table in [taxonomy.md](../../taxonomy.md)) that haven't been migrated. Per the Cross-Classification Mapping table in taxonomy.md, their 2025 equivalents are already used by a newer, differently-named entry in this same table: `ACCIDENT` (`TL0007`) → `TL0201` (see `STRUCTURE`), `BOAT CAPSIZE` (`TL0050`) → `TL0403` (see `DROWNING`), `EPIZOOTIC` (`BI0027`) → `BI0301` (see `ANIMAL DISEASE`), `EXPLOSION` (`TL0029`) → `TL0304` (see `EXPLOSIONS`), `LEAK` (`TL0030`) → `TL0301` (see `LEAK OR SPILL`), `STRUCT.COLLAPSE` (`TL0005`) → `TL0201` (see `STRUCTURE`).
>
> ‡ `EPIDEMIC`'s GLIDE code is corrected to `EP` here. The upstream `hazard_mapping` dict currently has `OT`, which conflicts with the Cross-Classification Mapping table in [taxonomy.md](../../taxonomy.md), where `BI0101` + `nat-bio-epi-dis` maps to GLIDE `EP`. See [IFRCGo/pystac-monty#201](https://github.com/IFRCGo/pystac-monty/pull/201#issuecomment-5475551864) for the upstream fix.

> [!NOTE]
> All three classification codes (GLIDE, EM-DAT, UNDRR-ISC 2025) should be included in the `monty:hazard_codes` array for maximum interoperability, when all three are available for that row. More specific [hazard codes](../../taxonomy.md#complete-2025-hazard-list) can be added following the characteristics of the event.

This mapping enables standardized hazard categorization while preserving DesInventar's original classification in the source properties.

##### Unmapped events

The following canonical DesInventar events have no hazard code mapping (`hazard_mapping` returns `None`, including `OTHER`/`OT - Other`-style catch-alls). Records with these event types — plus any raw `evento` value with neither an alias nor a direct mapping — are dropped entirely: no event, hazard, or impact item is produced for them.

`ANIN BOT`, `ARBOL CAIDO`, `AUTHER`, `BÚSQUEDA`, `Búsqueda`, `CAÍDA DE ARBOL`, `Caída de Arbol`, `CLIMATE CHANGE`, `Desaparecido (S)`, `DROPP OFF`, `EXTREME TEMPERATURE`, `FAILEN TREES`, `FALL INTO A WELL`, `FAMINE`, `Famine`, `Food Insecurity`, `Geomedical`, `Hambruna`, `HAILSTONE`, `HIGH TIDE`, `HUNGER/FAMINE`, `INDUSTRIAL DISASTER`, `LAINNYA`, `LALORAN BOOT`, `Livestock`, `Mal uvuljuulekh`, `MALNUTRITION`, `Malnutrition`, `Napolo`, `Nawaa`, `OT - Other`, `OTHER`, `OTHER_AC`, `Other`, `PANIC`, `PEAT`, `PORT AREA HAZARD`, `PROJECTILE`, `Rescate`, `RESCATE`, `Riverinflood`, `Road`, `Stormy`, `Stuck`, `TD - Technical Disaster`, `Traslados`, `TREE FALLEN`, `W`, `birds`, `incursion`

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
| [monty:impact_detail](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:impact_detail)                |                            | Object containing impact details                   |
| monty:impact_detail.category                                                                                | From mapping table         | Impact category code                               |
| monty:impact_detail.type                                                                                    | From mapping table         | Impact type code                                   |
| monty:impact_detail.value                                                                                   | From Desinventar field     | Numeric impact value                               |
| monty:impact_detail.unit                                                                                    | From mapping table         | Unit of measurement                                |
| monty:impact_detail.estimate_type                                                                           | "primary"                  | All Desinventar data is considered primary         |

The geometry, bbox, datetime and other base fields are inherited from the source event item.
