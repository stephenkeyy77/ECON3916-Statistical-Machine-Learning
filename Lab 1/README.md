# Global Purchasing Power Parity Analysis via the Big Mac Index

## Objective
This project applies the Law of One Price to assess currency valuation across international markets using The Economist's Big Mac Index as a proxy for purchasing power parity.

## Methodology
* **Data Construction**: Manually structured a cross-sectional dataset from The Economist's 2015 Big Mac pricing data across multiple currencies and geographic markets
* **PPP Calculation**: Computed implied purchasing power parity exchange rates by normalizing local Big Mac prices against the US benchmark price
* **Valuation Analysis**: Derived percentage deviations between implied PPP rates and actual market exchange rates to identify currency over/undervaluation relative to the US Dollar

## Key Findings
[Replace with your specific results. Example framework below:]

The analysis revealed significant currency misalignments against the US Dollar baseline. The Norwegian Krone exhibited overvaluation of approximately X%, suggesting potential arbitrage opportunities or structural market inefficiencies. Conversely, [currency name] demonstrated undervaluation of Y%, indicating purchasing power disparity relative to the dollar-denominated benchmark. These deviations from parity reflect a combination of non-tradable service costs, market frictions, and macroeconomic fundamentals that prevent absolute price convergence across borders.

## Economic Interpretation
The Big Mac Index serves as an accessible illustration of PPP theory limitations in practice. While the Law of One Price theoretically predicts price convergence for identical goods, real-world deviations persist due to transportation costs, trade barriers, local input price differentials, and varying tax regimes—factors that this "burgernomics" approach effectively captures through a single standardized commodity.

---

**Technical Stack**: Python, Pandas
