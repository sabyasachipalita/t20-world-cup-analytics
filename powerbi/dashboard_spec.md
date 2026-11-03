# Power BI Dashboard Visual Design Specification

## Page 1: Tournament Executive Summary & KPIs
* **Top Header:** "2022 ICC Men's T20 World Cup Analytics" + Slicers for `Team`, `Venue / Ground`, `Stage`.
* **KPI Card 1:** Total Matches Played (`COUNTROWS(dim_matches)`).
* **KPI Card 2:** Total Runs Scored (`[Total Runs]`).
* **KPI Card 3:** Tournament Boundary Count (`[Fours] + [Sixes]`).
* **KPI Card 4:** Total Wickets Fallen (`[Total Wickets]`).
* **KPI Card 5:** Global Strike Rate (`[Batting Strike Rate]`).
* **Chart 1 (Donut Chart):** Match Wins Distribution by Margin Type (Runs vs Wickets vs DLS).
* **Chart 2 (Clustered Bar Chart):** Runs scored per Venue / Ground.
* **Chart 3 (Leaderboard Table):** Top 10 run scorers & top 10 wicket takers.

---

## Page 2: Batting Performance & Phase Strategy
* **Visual 1 (Scatter Plot - Batter Archetypes):**
  * X-axis: `[Batting Strike Rate]`
  * Y-axis: `[Batting Average]`
  * Size: `[Total Runs]`
  * Legend: `dim_players[playingRole]`
  * Tooltips: `Player Name`, `Boundary %`, `Sixes`
  * *Quadrant Insight:* Top-Right quadrant represents elite tournament match-winners (Virat Kohli, Suryakumar Yadav).
* **Visual 2 (Stacked Bar Chart):** Run Composition (Boundary Runs vs Running Between Wickets).
* **Visual 3 (Table with Data Bars):**
  * Columns: Player Name, Team, Total Runs, Strike Rate, Average, Boundary %, 50s.

---

## Page 3: Bowling Mastery & Death-Over Impact
* **Visual 1 (Quadrant Bubble Chart):**
  * X-axis: `[Bowling Economy Rate]` (Reverse axis so lower economy is on the right)
  * Y-axis: `[Dot Ball %]`
  * Bubble Size: `[Total Wickets]`
  * Legend: `dim_players[bowlingStyle]`
  * *Elite Zone:* High dot-ball percentage (>50%) and low economy (<6.5) (Sam Curran, Anrich Nortje, Shaheen Afridi).
* **Visual 2 (Horizontal Bar Chart):** Leading Wicket-Takers sorted by Wickets with Economy data labels.
* **Visual 3 (Decomposition Tree / Drilldown):** Bowling Team $\rightarrow$ Bowler $\rightarrow$ Dismissal types.

---

## Page 4: Data-Driven "Best XI" Selection
* **Visual 1 (Interactive Team Formation Grid - Cricket Pitch Visual):**
  * Openers (Slots 1-2): Jos Buttler (C/WK), Alex Hales
  * Top Order (Slot 3): Virat Kohli
  * Middle Order (Slot 4): Suryakumar Yadav
  * Middle Order / Finisher (Slot 5): Glenn Phillips
  * All-Rounders (Slots 6-7): Shadab Khan, Sam Curran (POTS)
  * Spin Specialist (Slot 8): Wanindu Hasaranga
  * Pace Trio (Slots 9-11): Anrich Nortje, Shaheen Shah Afridi, Arshdeep Singh
* **Visual 2 (Radar / Spider Chart):** Team Best XI aggregate balance (Powerplay Strike Rate vs Death Bowling Economy vs Spin Control).
