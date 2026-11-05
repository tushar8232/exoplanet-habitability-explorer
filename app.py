
import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Exoplanet Habitability Explorer",
    page_icon="🪐",
    layout="wide"
)

# Load dataset
df = pd.read_csv("data/processed/final_candidate_summary.csv")
screening_df = pd.read_csv("data/processed/final_exoplanet_screening.csv")

# Title
st.title("🪐 Exoplanet Habitability Explorer")
st.write(
    "Explore exoplanets screened using conservative "
    "and optimistic habitable-zone models."
)

# Metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total HZ Candidates", len(df))

col2.metric(
    "Conservative HZ",
    (df["final_hz_category"] == "Conservative HZ").sum()
)

col3.metric(
    "Optimistic-only HZ",
    (df["final_hz_category"] == "Optimistic-only HZ").sum()
)

st.divider()

# Category filter
st.subheader("Explore Candidates")

category = st.selectbox(
    "Select HZ category",
    ["All", "Conservative HZ", "Optimistic-only HZ"]
)

if category == "All":
    filtered_df = df.copy()
else:
    filtered_df = df[
        df["final_hz_category"] == category
    ]

# Small-radius filter
small_only = st.checkbox(
    "Show only planets with radius ≤ 1.6 Earth radii"
)

if small_only:
    filtered_df = filtered_df[
        filtered_df["pl_rade"] <= 1.6
    ]

# Search
search = st.text_input("Search planet name")

if search:
    filtered_df = filtered_df[
        filtered_df["pl_name"].str.contains(
            search, case=False, na=False
        )
    ]

# Display results
st.write(f"Showing {len(filtered_df)} candidates")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Screening results are not confirmation of habitability "
    "or evidence of life."
)

st.divider()

st.subheader("📊 Candidate Analytics")

# Chart 1: HZ category distribution
st.write("### Habitable Zone Distribution")

category_counts = df["final_hz_category"].value_counts()

st.bar_chart(category_counts)

# Chart 2: Planet radius distribution
st.write("### Planet Radius Distribution")

import matplotlib.pyplot as plt

fig, ax = plt.subplots()

ax.hist(
    df["pl_rade"],
    bins=10,
    edgecolor="black"
)

ax.set_xlabel("Planet Radius (Earth radii)")
ax.set_ylabel("Number of Planets")
ax.set_title("Distribution of Planetary Radii")

st.pyplot(fig)
plt.close(fig)

# Chart 3: Discovery method distribution
st.write("### Discovery Methods")

method_counts = df["discoverymethod"].value_counts()

st.bar_chart(method_counts)


st.divider()

st.subheader("🔬 Compare Two Exoplanets")

planet_names = sorted(df["pl_name"].unique())

col1, col2 = st.columns(2)

with col1:
    planet1 = st.selectbox(
        "Select first planet",
        planet_names,
        key="planet1"
    )

with col2:
    planet2 = st.selectbox(
        "Select second planet",
        planet_names,
        index=1,
        key="planet2"
    )

p1 = df[df["pl_name"] == planet1].iloc[0]
p2 = df[df["pl_name"] == planet2].iloc[0]

comparison = pd.DataFrame({
    "Property": [
        "Host Star",
        "Planet Radius (Earth radii)",
        "Equilibrium Temperature (K)",
        "Insolation Flux (Earth units)",
        "Orbital Distance (AU)",
        "Stellar Temperature (K)",
        "HZ Category"
    ],
    planet1: [
        p1["hostname"],
        p1["pl_rade"],
        p1["pl_eqt"],
        p1["pl_insol"],
        p1["pl_orbsmax"],
        p1["st_teff"],
        p1["final_hz_category"]
    ],
    planet2: [
        p2["hostname"],
        p2["pl_rade"],
        p2["pl_eqt"],
        p2["pl_insol"],
        p2["pl_orbsmax"],
        p2["st_teff"],
        p2["final_hz_category"]
    ]
})

st.dataframe(
    comparison,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.subheader("🌍 Why Is This Planet in the Habitable Zone?")

# Load detailed screening results containing HZ boundaries
screening_df = pd.read_csv("data/processed/final_exoplanet_screening.csv")

planet = st.selectbox(
    "Choose a planet to investigate",
    sorted(screening_df["pl_name"].dropna().unique()),
    key="hz_explanation_planet"
)

p = screening_df[
    screening_df["pl_name"] == planet
].iloc[0]

st.write(f"### {planet}")

st.write(
    f"**Classification:** {p['final_hz_category']}"
)

st.metric(
    "Planet's orbital distance",
    f"{p['pl_orbsmax']:.5f} AU"
)

# Display HZ boundaries
boundaries = pd.DataFrame({
    "Boundary": [
        "Recent Venus (optimistic inner)",
        "Runaway Greenhouse (conservative inner)",
        "Maximum Greenhouse (conservative outer)",
        "Early Mars (optimistic outer)"
    ],
    "Distance (AU)": [
        p["hz_recent_venus_au"],
        p["hz_runaway_greenhouse_au"],
        p["hz_maximum_greenhouse_au"],
        p["hz_early_mars_au"]
    ]
})

st.write("### Calculated Habitable Zone Boundaries")

st.dataframe(
    boundaries,
    use_container_width=True,
    hide_index=True
)

st.info(
    "The conservative HZ lies between the runaway greenhouse "
    "and maximum greenhouse boundaries. The optimistic HZ "
    "lies between recent Venus and early Mars boundaries."
)

st.divider()

st.subheader("🪐 Orbital Position in the Habitable Zone")

import matplotlib.pyplot as plt

# Read orbital and HZ boundary distances
orbit = p["pl_orbsmax"]
recent = p["hz_recent_venus_au"]
runaway = p["hz_runaway_greenhouse_au"]
maximum = p["hz_maximum_greenhouse_au"]
mars = p["hz_early_mars_au"]

if all(pd.notna(x) for x in [orbit, recent, runaway, maximum, mars]):

    fig, ax = plt.subplots(figsize=(10, 3))

    # Optimistic HZ region
    ax.axvspan(
        recent, mars,
        alpha=0.2,
        label="Optimistic HZ"
    )

    # Conservative HZ region
    ax.axvspan(
        runaway, maximum,
        alpha=0.4,
        label="Conservative HZ"
    )

    # Planet orbital position
    ax.axvline(
        orbit,
        color="red",
        linestyle="--",
        linewidth=2,
        label="Planet Orbit"
    )

    ax.set_xlabel("Distance from Star (AU)")
    ax.set_yticks([])
    ax.set_title(f"Orbital Position: {planet}")
    ax.legend()
    ax.grid(axis="x", alpha=0.3)

    st.pyplot(fig)
    plt.close(fig)

else:
    st.warning("Insufficient data to visualize this planet's orbit.")



st.divider()

st.header("📚 Methodology and Scientific Limitations")

st.subheader("1. Data Source")

st.write(
    "The project uses planetary and stellar parameters "
    "from the NASA Exoplanet Archive Planetary Systems "
    "Composite Parameters dataset."
)

st.subheader("2. Stellar Luminosity")

st.latex(
    r"\\frac{L}{L_\\odot} = "
    r"\\left(\\frac{R}{R_\\odot}\\right)^2 "
    r"\\left(\\frac{T}{5772}\\right)^4"
)

st.write(
    "Stellar luminosity is estimated using stellar radius "
    "and effective temperature."
)

st.subheader("3. Habitable Zone Calculation")

st.write(
    "The project applies the temperature-dependent "
    "Kopparapu habitable-zone model using the "
    "1 Earth-mass coefficient set."
)

st.write(
    "The conservative zone is bounded by the runaway "
    "greenhouse and maximum greenhouse limits."
)

st.write(
    "The optimistic zone is bounded by the recent Venus "
    "and early Mars limits."
)

st.subheader("4. Candidate Screening")

st.write(
    "Planets are screened by comparing their orbital "
    "semi-major axis with the calculated habitable-zone "
    "boundaries. A radius threshold of 1.6 Earth radii "
    "is used to identify small-radius candidates."
)

st.subheader("5. Important Limitations")

limitations = [
    "Being inside the habitable zone does not prove that a planet is habitable.",
    "Atmospheric composition and surface conditions are not established.",
    "Planetary eccentricity is not incorporated into the orbital-position screening.",
    "The luminosity calculation uses estimated stellar parameters.",
    "The habitable-zone model uses a 1 Earth-mass assumption.",
    "The simplified radius threshold does not prove that a planet is rocky.",
    "The machine-learning labels are rule-based screening labels, not confirmed habitability measurements."
]

for item in limitations:
    st.warning(item)
