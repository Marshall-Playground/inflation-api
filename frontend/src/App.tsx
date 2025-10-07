import { useState } from "react";

function App(): JSX.Element {
  const [year, setYear] = useState<number>(2020);

  return (
    <main className="app">
      <header>
        <h1>Inflation Calculator</h1>
        <p>
          Lightweight client for the Inflation API. Configure the API base URL via environment
          settings once wiring is complete.
        </p>
      </header>

      <section className="card">
        <label htmlFor="year-input">Year</label>
        <input
          id="year-input"
          type="number"
          min={1913}
          max={2100}
          value={year}
          onChange={(event) => setYear(Number.parseInt(event.target.value, 10))}
        />
        <p className="hint">API integration to be added in the next phase.</p>
      </section>
    </main>
  );
}

export default App;
