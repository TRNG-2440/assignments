# Architecture Overview

1. Data input coped to raw folder
2. Input folder loaded in, ingestion columns added before being added to bronze layer.
3. Silver layer processes and validates data using refences from master spreadsheet.
4. Silver data loaded into gold layer for analytical insights.
5. Overwrite option used for saving files to medallion layers.
