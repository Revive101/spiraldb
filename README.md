# spiraldb

## BadgeDefinitions

One file per badge: `BadgeDefinitions/badgedefinitions_<Id>.json`, where `<Id>` is the numeric badge id the client sees
(the `StringHash` of the badge's internal name). 2046 records, keyed by `Id`.

Properties of a record, in file order:

| property | meaning |
|---|---|
| `Id` | `m_badgeNameID` (unique) |
| `Name` | internal badge name, or `null` when unknown (1765 of 2046); when set, `StringHash(Name) == Id` |
| `DisplayName`, `Description` | English title and rule text, for humans only |
| `Title`, `Info`, `ProgressInfo` | locale keys sent to the client (`m_badgeTitle`, `m_badgeInfo`, `m_badgeProgressInfo`); tiers of one counter family share `ProgressInfo` |
| `Max` | target count (0 for one-shot badges) |
| `Index` | the client's slot key (`m_index`), unique among non-dynamic records |
| `Outline`, `Image` | art paths, kept verbatim |
| `Dynamic`, `ExtraCredit` | `m_dynamicBadge`, `m_extraCredit` |
| `Filter` | category name; the client filter id is `StringHash(Filter)` |
| `ShowTitle`, `Retired` | server flags (`ShowTitle` is true everywhere; `Retired` is set on one badge) |
| `HasReward`, `RewardOverrideDescription`, `Overcount`, `OvercountInterval` | informational reward data; badge rewards are not served yet |
| `RewardLootTable`, `OvercountLootTable` | reserved, `null` |
| `RegistryName`, `Adjectives`, `AutoAdd`, `Requirements`, `RequiredAutoAddBadges`, `CompleteResults` | earn rules; empty except for the families under "Earn rules". A record without a rule is catalog-only |

Player state (`m_badgeComplete`, `m_badgeProgress`, `m_originalProgress`) is not stored, and neither are the byte-shifted
`m_badgeFilterID` / `m_filterIndex`: the filter is the category name, matched by hash against the names in `BadgeFilterDescriptions.xml`.
`Name` is set only where a candidate name hashes to `Id` (`m_badgeName` strings in the game's object and spell data, quest `ResAddBadge` names,
the names the client uses itself, `<School>Weaving-Level0N`).

To change a record, edit its file by hand; records are keyed by `Id`.

Not included: 10 pages whose live id cannot be recovered (the 1st and 2nd Age Pet Derby ranks, `Hometown Hero`, `Associate Delivery Person`,
`Added All the Dryads`). The 30 Balance Weaving pages were re-keyed to the id of their real internal name
(`BalanceWeaving-Level01..05`, `BalanceWeaving-QuestNN-TaskNN`) and given `Index` values above the highest of the other records (5006).

### Earn rules

Earn rules are authored separately and merged into the records (`Adjectives`, `RegistryName`, `AutoAdd`, `Requirements`,
`RequiredAutoAddBadges`, `CompleteResults`), one family at a time, each with its evidence. A record without a rule is catalog-only: play never changes it.
The counter key of a family is `RegistryName` when set, else the `ProgressInfo` its tiers share, else the decimal `Id`.

| family | records | rule | counter key |
|---|---|---|---|
| Undead | 10 tiers, `Max` 50 to 20000 (`1623459278` Undead Stalker to `1757677006` Undead Executioner) | `Adjectives ["Undead"]` | `Badges_00002780` |
| Krok | 3 tiers, `Max` 50, 100, 200 (`1721059392`, `1721051200`, `1721043008`) | `Adjectives ["Krok"]` | `Badges_00004661` |

Evidence: the counter label text (`Badges_00002780` reads "Undead", `Badges_00004661` reads "Kroks"), the adjective on the object templates (`Undead` on 689 template files, `Krok` on 118),
and the captured badge updates after a victory (`quests/quest1_cleaned.json` #674, Undead Stalker 1/50; `quests/quest4_cleaned.json` #16850 and #16851, Krok Hunter and Krok Thrasher).
The mapping from adjective to badge is inferred, not read from game data. The check in game: after the kill path exists, defeating a Lost Soul shows Undead Stalker 1/50.
