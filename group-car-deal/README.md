# GroupDiive

A local app for comparing car offers for a group of buyers in India. See [demo script](DEMO_SCRIPT.md) for a short walkthrough and the [design reference](docs/GROUP_CAR_DEAL_UI_PROMPT.md).

## Local sample car catalog

Car information is stored in `data/cars.json`. It is sample data, so check prices
and details with the car maker before making a decision.

Run `python data/load_cars.py` to copy the JSON catalog into SQLite. The seed
script does this automatically. To add cars from a CSV file, use
`python data/import_cars.py path/to/cars.csv`. The CSV columns are `brand`,
`model`, `body_type`, `fuel_types`, `launch_year`, `model_years_available`, and
`variants`. Put JSON lists in the `fuel_types`, `model_years_available`, and
`variants` columns. Empty optional values can be left blank.

## Location estimates

The state and city list and sample RTO and insurance estimate rates are in
`config/india_locations.json`. Edit those rates to change the simple calculator.
They are estimates only; real charges vary by vehicle and local rules. The
dealer offer form keeps the charges entered by each dealer separate.

## Run locally

Create and activate a virtual environment, install the packages, and start the
Home page:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
streamlit run app.py
```

The app's pages are in `pages/`. It uses the local SQLite file and catalog; it
does not scrape car websites or load car photos from external sites. Catalog
prices and seeded offers are demo data. The local AI needs Ollama running with
the model named in `.env`, but the rest of the app works when Ollama is off.
