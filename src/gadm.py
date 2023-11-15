import geopandas as gpd
import pandas as pd

countries_and_codes = {
    "American Samoa": "ASM",
    "Cook Islands": "COK",
    "Fiji": "FJI",
    "French Polynesia": "PYF",
    "Guam": "GUM",
    "Kiribati": "KIR",
    "Marshall Islands": "MHL",
    "Micronesia": "FSM",
    "Nauru": "NRU",
    "New Caledonia": "NCL",
    "Niue": "NIU",
    "Northern Mariana Islands": "MNP",
    "Palau": "PLW",
    "Papua New Guinea": "PNG",
    "Pitcairn Islands": "PCN",
    "Solomon Islands": "SLB",
    "Samoa": "WSM",
    "Tokelau": "TKL",
    "Tonga": "TON",
    "Tuvalu": "TUV",
    "Vanuatu": "VUT",
    "Wallis and Futuna": "WLF",
}

all_polys = pd.concat(
    [
        gpd.read_file(
            f"https://geodata.ucdavis.edu/gadm/gadm4.1/gpkg/gadm41_{code}.gpkg"
        )
        for code in countries_and_codes.values()
    ]
)

all_polys.to_file("data/gadm_pacific.gpkg")
all_polys.dissolve("COUNTRY").to_file("data/gadm_pacific_union.gpkg")
