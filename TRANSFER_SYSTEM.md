# Transfer System - Fantasy Football League

## Overview

The transfer system allows students to modify their squad throughout the Premier League season. To maintain strategic balance and prevent constant squad changes, each team is limited to **2 transfers per gameweek**.

## What is a Transfer?

A transfer occurs when you swap one player out of your team for another player. This includes:
- **Removing and Adding:** When you remove a player and add a new one
- **Player Swaps:** Direct replacements to fill squad slots
- **Positional Changes:** Swapping players of different positions

## Transfer Limit

### Maximum: 2 Transfers Per Gameweek

- Each gameweek resets your transfer count to 0
- You can make up to 2 player changes per gameweek
- When you hit the limit, you cannot make more changes until the next gameweek

### Tracking Your Transfers

In the **Manage Squad** page, you'll see:
```
⚡ Transfers: 1/2 used
   1 transfer remaining
```

The counter shows:
- **Used Transfers:** How many transfers you've made in the current gameweek (0-2)
- **Remaining Transfers:** How many more you can make (0-2)
- **Status Message:**
  - ✅ Green: You have transfers available
  - ⚠️ Red: You've reached your 2-transfer limit

## Why This Limit?

### Educational Benefits

1. **Strategic Thinking:** Students must plan squad changes carefully rather than making impulsive swaps
2. **Decision Making:** Forces analysis of player form, upcoming fixtures, and team needs
3. **Real-World Simulation:** Mirrors the actual Fantasy Premier League system used by millions
4. **Squad Management:** Teaches long-term planning and balancing immediate needs with season strategy

### Game Balance

- Prevents constantly changing teams
- Makes leagues competitive and challenging
- Adds a strategic layer beyond just picking good players
- Encourages holding players and managing form

## Gameweek Reset

The transfer count resets automatically at the start of each new gameweek:
- **Gameweek 1:** You start with 2 transfers available
- **After GW1 ends:** Your transfer count resets
- **Gameweek 2:** You have 2 new transfers available
- This continues throughout the entire season

## Tips for Squad Management

### Making the Most of Your Transfers

1. **Plan Ahead:**
   - Look at upcoming fixtures
   - Identify players with good form
   - Plan 2-3 gameweeks ahead

2. **Monitor Player Form:**
   - Check points from recent weeks
   - Look for in-form players
   - Avoid injured players

3. **Use Transfers Strategically:**
   - Don't waste transfers on minor improvements
   - Save them for important swaps
   - Consider the cost of removing players (can affect team value)

4. **Track the Schedule:**
   - Easy fixtures coming up?
   - Important matches this week?
   - Plan transfers around the fixture list

## Example Scenario

**Gameweek 5:**
- You have 2 transfers available
- Your striker is injured
- You notice an in-form midfielder

**Action Plan:**
- Transfer 1: Remove injured striker, add fit replacement
- Transfer 2: Remove out-of-form midfielder, add in-form player
- You're now at 2/2 transfers used
- Wait until Gameweek 6 for more transfers

## Technical Details

### Transfer Tracking

Each transfer is logged with:
- **Player Out:** The player you removed
- **Player In:** The player you added
- **Gameweek:** When the transfer was made
- **Timestamp:** Exact date/time of transfer

### Preventing Over-Transfers

The system automatically prevents making more than 2 transfers per gameweek:
- Form validation checks your transfer count
- If you try to exceed 2, you'll see an error message
- You must wait until the next gameweek to continue

## FAQs

**Q: Can I use a transfer from last gameweek?**
A: No, transfers are per-gameweek only. They reset automatically.

**Q: What happens if I reach the transfer limit mid-gameweek?**
A: You can still add/remove players initially, but once you hit 2 transfers, you're locked until next gameweek.

**Q: Can the admin reset my transfers?**
A: Yes, league admins or teachers can adjust gameweek numbers if needed for special circumstances.

**Q: Do trades/loans count as transfers?**
A: Currently, the system only tracks direct player swaps as transfers.

**Q: Can I see my transfer history?**
A: Yes, your Transfer History page shows all swaps made this season, organized by gameweek.

## For Teachers/Admins

### Managing Transfers

To manage transfers in the admin panel:

1. **View Transfers:**
   - Go to Admin > Transfers
   - See all transfers made by all teams

2. **Filter by:**
   - Team
   - Gameweek
   - Date range

3. **Advance Gameweek:**
   - Update `current_gameweek` field on UserTeam
   - This resets transfer counts automatically

### Tips for Managing the League

- **Start of Season:** Confirm all students understand the 2-transfer limit
- **Monitoring:** Watch for patterns (teams constantly at their limit suggests active engagement)
- **Weekly Updates:** Update the gameweek at the official Premier League cutoff time (typically Friday 3 PM GMT)

---

**Last Updated:** January 2026
**Version:** 1.0
