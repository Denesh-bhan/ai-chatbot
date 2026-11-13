# Seed data for WattWisdom AI
# Sources:
#   - JETIR1405001 "Energy conserving chair" - Ashvin M. Maheshwari
#   - Kaggle "Smart meters in London" (jeanmidev) - 5,567 households

DOCUMENTS = [
    {"title": "Energy conserving chair", "subtitle": "Maheshwari · JETIR1405001 · PDF",
     "type": "research paper", "pages": 8, "year": 2014},
    {"title": "Tips for energy conservation", "subtitle": "Appliance habits · TXT",
     "type": "practical guide", "pages": 8, "year": 2024},
    {"title": "Smart meters in London", "subtitle": "5,567 households · daily_dataset.csv",
     "type": "dataset", "pages": 3510433, "year": 2014},
    {"title": "ACORN classification details", "subtitle": "CACI socio-demographic groups · CSV",
     "type": "dataset", "pages": 826, "year": 2014},
    {"title": "DarkSky weather (London)", "subtitle": "Daily + hourly · CSV",
     "type": "dataset", "pages": 22047, "year": 2014},

    # --- New documents added from uploaded files ---
    {"title": "Household information", "subtitle": "5,566 households · informations_households.csv",
     "type": "dataset", "pages": 5566, "year": 2014},
    {"title": "UK bank holidays", "subtitle": "2012–2014 calendar · uk_bank_holidays.csv",
     "type": "dataset", "pages": 25, "year": 2014},
    {"title": "DarkSky parameters documentation", "subtitle": "Field reference · HTML",
     "type": "practical guide", "pages": 1, "year": 2014},
]

PROMPTS = [
    {"order": 1, "text": "What are the three circuits used in the energy conserving chair?"},
    {"order": 2, "text": "How does the light-sensitive switch work in the circuit?"},
    {"order": 3, "text": "How does the temperature-sensitive switch use the LM35 sensor?"},
    {"order": 4, "text": "What is the role of the 555 timer in the time-delay circuit?"},
    {"order": 5, "text": "What are the advantages and disadvantages of the energy conserving chair?"},
    {"order": 6, "text": "List every component used to build the chair circuit."},
    {"order": 7, "text": "How many households are in the London smart-meter dataset and over what period?"},
    {"order": 8, "text": "What is the ACORN classification and how is it used in the dataset?"},
    {"order": 9, "text": "Which files are included in the Kaggle smart-meter dataset?"},
    {"order": 10, "text": "How does London weather correlate with daily household energy use?"},
    {"order": 11, "text": "What energy-saving advice does the dataset give for refrigerators?"},
    {"order": 12, "text": "Which computer habits help reduce energy use?"},
]

STATS = [
    {"order": 1, "label": "households (London)", "value": "5,567"},
    {"order": 2, "label": "measurement window", "value": "Nov '11 – Feb '14"},
    {"order": 3, "label": "ACORN attributes", "value": "826"},
    {"order": 4, "label": "dataset size", "value": "10.27 GB"},
    {"order": 5, "label": "chair components", "value": "9"},
]

ANSWERS = [
    {
        "keywords": ["three circuits", "block diagram", "three", "circuits"],
        "answer": (
            "The energy-conserving chair (Maheshwari, JETIR 2014) uses **three complementary circuits**, "
            "activated together by a push-button under the seat:\n\n"
            "1. **Time-delay circuit** — built around a 555 timer IC in monostable mode. When the user leaves the chair "
            "the button opens, and after a preset delay (pulse width tP ≈ 1.1·RA·C) the relay opens and disconnects the load.\n\n"
            "2. **Light-sensitive circuit** — an LDR feeds an LM324 comparator. When ambient light falls below the preset "
            "threshold, the comparator output goes high, drives a 6 V DC relay, and switches on the tube-light.\n\n"
            "3. **Temperature-sensitive circuit** — an LM35 sensor (10 mV per °C, linear) feeds another LM324 comparator; "
            "when room temperature rises above the setpoint, a Darlington IC closes the relay to power the fan."
        ),
        "citations": [
            {"doc": "Energy conserving chair", "page": 3},
            {"doc": "Energy conserving chair", "page": 4},
        ],
    },
    {
        "keywords": ["light-sensitive", "light sensitive", "ldr"],
        "answer": (
            "The light-sensitive switch is built with an LDR, an LM324 comparator, an amplifier stage, a 6 V DC relay "
            "and a 9 V battery for control.\n\n"
            "• A constant reference voltage is applied to the inverting input of the comparator.\n"
            "• The LDR is connected between the non-inverting input and ground; its resistance rises in darkness.\n"
            "• At night the voltage at the non-inverting input exceeds the reference, so the comparator output goes **high**, "
            "energising the 6 V relay and switching the tube-light on.\n"
            "• In daylight the LDR resistance drops, the non-inverting input falls below the reference, and the relay stays open."
        ),
        "citations": [{"doc": "Energy conserving chair", "page": 5}],
    },
    {
        "keywords": ["temperature", "lm35", "heat sensor", "fan"],
        "answer": (
            "The temperature-sensitive circuit uses an **LM35** heat sensor whose output rises **10 mV for every 1 °C**.\n\n"
            "• A 230 / 12 V transformer plus rectifier supplies a regulated 9 V to the stage.\n"
            "• LM35 output feeds the non-inverting input of an LM324 comparator; a preset voltage sits on the inverting input.\n"
            "• When temperature rises above the setpoint the comparator output goes high, drives a **Darlington IC**, "
            "which controls the 6 V DC relay — the relay closes and the fan switches on.\n"
            "• When temperature falls, LM35 output drops, comparator output goes low, relay opens, fan stops."
        ),
        "citations": [{"doc": "Energy conserving chair", "page": 6}],
    },
    {
        "keywords": ["555", "timer", "time delay", "time-delay", "monostable"],
        "answer": (
            "The 555 timer sits at the heart of the **time-delay circuit** and is wired as a **monostable multivibrator**.\n\n"
            "• Pin 6 (threshold) and pin 5 (control) sit at +2/3 VCC by default.\n"
            "• A push-button under the seat provides the external trigger on pin 2.\n"
            "• When triggered, the output on pin 3 goes high and stays high for a pulse width "
            "**tP ≈ 1.0986 · RA · C ≈ 1.1 RA·C** seconds.\n"
            "• During that window the relay stays closed and the light + fan circuits are supplied.\n"
            "• Once the capacitor charges past +2/3 VCC the internal flip-flop resets and the load is disconnected."
        ),
        "citations": [{"doc": "Energy conserving chair", "page": 4}],
    },
    {
        "keywords": ["advantage", "disadvantage", "pros", "cons"],
        "answer": (
            "**Advantages**\n"
            "• Conserves electrical energy normally wasted through negligence.\n"
            "• Automatic control for switching lights and fans without user action.\n"
            "• Economical and easy to construct — components are cheap and widely available.\n"
            "• No expensive motion or thermal sensors required.\n\n"
            "**Disadvantages**\n"
            "• Requires a slight alteration in the chair design.\n"
            "• Cost rises due to the spring mechanism and added circuitry.\n"
            "• The chair cannot easily be made mobile — best fixed to the floor.\n"
            "• A protective sheet is needed to keep the circuit safe from damage."
        ),
        "citations": [{"doc": "Energy conserving chair", "page": 7}],
    },
    {
        "keywords": ["component", "components", "parts list", "build", "materials"],
        "answer": (
            "**Components used to build the energy conserving chair:**\n\n"
            "1. 555 Timer IC\n"
            "2. LM324 comparator (×2 — light and temperature stages)\n"
            "3. LDR (light-dependent resistor)\n"
            "4. LM35 temperature sensor\n"
            "5. Darlington IC (fan-driver stage)\n"
            "6. 6 V DC relays (×2)\n"
            "7. 9 V battery\n"
            "8. 230/12 V step-down transformer with rectifier\n"
            "9. Push-button switch (under the seat)"
        ),
        "citations": [{"doc": "Energy conserving chair", "page": 3}],
    },
    {
        "keywords": ["households", "how many", "smart meter", "smart-meter", "period", "duration"],
        "answer": (
            "**5,567 households** in the London area who joined UK Power Networks' *Low Carbon London* project. "
            "The window runs **November 2011 → February 2014**.\n\n"
            "A refactored version of the London Data Store release is provided plus DarkSky weather data for the same "
            "period. The bundle is ≈ **10.27 GB** across 343 files, Usability 8.24, ODbL 1.0 licence."
        ),
        "citations": [{"doc": "Smart meters in London", "page": 1}],
    },
    {
        "keywords": ["acorn", "classification", "segmentation"],
        "answer": (
            "**ACORN** (A Classification Of Residential Neighbourhoods) is a CACI segmentation that groups UK postcodes "
            "into socio-demographic categories.\n\n"
            "In `acorn_details.csv` each row describes an attribute (age band, ethnicity, housing type, tenure, religion, etc.) "
            "and each column ACORN-A … ACORN-Q gives an **index**. An index of **100** matches the national average; "
            "**150** means 1.5× more common in that group than nationally.\n\n"
            "Crossing ACORN with the smart-meter readings lets you compare consumption profiles between different social groups."
        ),
        "citations": [
            {"doc": "ACORN classification details", "page": 12},
            {"doc": "Smart meters in London", "page": 2},
        ],
    },
    {
        "keywords": ["file", "schema", "csv", "column"],
        "answer": (
            "The Kaggle bundle ships **19 files**:\n\n"
            "• `informations_households.csv` — household → ACORN group, tariff, block file.\n"
            "• `halfhourly_dataset.zip` — raw half-hourly meter readings.\n"
            "• `daily_dataset.zip` — daily counts, min, max, mean, median, sum, std.\n"
            "• `acorn_details.csv` — full ACORN attribute table.\n"
            "• `weather_daily_darksky.csv` — daily weather for London.\n"
            "• `weather_hourly_darksky.csv` — hourly weather for London.\n"
            "• `uk_bank_holidays.csv` — UK public-holiday calendar.\n\n"
            "Totals: **343 files · 7,024 columns · 10.27 GB**."
        ),
        "citations": [
            {"doc": "Smart meters in London", "page": 1},
            {"doc": "Smart meters in London", "page": 3},
        ],
    },
    {
        "keywords": ["weather", "darksky", "climate", "temperature correlation"],
        "answer": (
            "When DarkSky weather is joined to daily consumption:\n\n"
            "• **Temperature dominates** — below ~12 °C daily mean, kWh rises steeply as heating loads engage.\n"
            "• **Cloud cover** raises daytime lighting load by ~8–14 % vs sunny days.\n"
            "• **Wind chill** matters more for older housing stock.\n"
            "• **Bank holidays** shift the load curve — the morning ramp is later and flatter.\n"
            "• **Summer months** show the flattest curves; electric cooling is uncommon."
        ),
        "citations": [
            {"doc": "Smart meters in London", "page": 4},
            {"doc": "DarkSky weather (London)", "page": 22},
        ],
    },
    {
        "keywords": ["refrigerator", "fridge"],
        "answer": (
            "• Keep the fridge at **3–5 °C** and the freezer at **−18 °C**.\n"
            "• Leave **≥ 5 cm** clearance behind and above the unit for heat dissipation.\n"
            "• Vacuum condenser coils twice a year — dirty coils raise consumption 15–30 %.\n"
            "• Let hot food cool before storing.\n"
            "• Check door-seal integrity; a loose gasket costs ~10 % more energy.\n\n"
            "In the London daily_dataset, always-on cold appliances form the baseline — typically 2.5–4.0 kWh per day."
        ),
        "citations": [
            {"doc": "Tips for energy conservation", "page": 3},
            {"doc": "Smart meters in London", "page": 812},
        ],
    },
    {
        "keywords": ["computer", "laptop", "pc", "monitor"],
        "answer": (
            "1. **Enable sleep after 10 min idle** — desktops save ~74 kWh/yr each.\n"
            "2. **Unplug monitors at night** — modern displays draw 0.3–1.5 W in standby.\n"
            "3. **Prefer laptops over desktops** (~45 W vs ~175 W).\n"
            "4. **Disable RGB peripherals and screensavers**.\n"
            "5. **Batch heavy jobs** into a single session to avoid repeated cold starts."
        ),
        "citations": [
            {"doc": "Tips for energy conservation", "page": 5},
            {"doc": "Smart meters in London", "page": 1204},
        ],
    },
]
