# Local AI Music MV Engineering System

This is the reusable method.

The goal is to turn any song into a repeatable production pipeline:

```text
song -> emotional map -> visual world -> asset library -> shot plan -> generated clips -> edit -> review -> repaired final
```

## The Five Layers

### 1. Song Analysis

You cannot make a strong MV until you know what the song is doing.

Extract:

- BPM or rough tempo
- intro / verse / pre-chorus / chorus / bridge / outro
- emotional curve
- strongest lyric images
- beat drops and transition points

### 2. Visual World

Choose one coherent world for the song.

Define:

- lead character
- costume language
- environment language
- color palette
- light logic
- camera personality

### 3. Asset Library

Create references before video generation.

Minimum:

- character identity
- costume
- stage/environment
- close-up inserts
- title/logo
- music reference

### 4. Shot Factory

Generate clips one shot at a time.

Every shot must have:

- reference image(s)
- action
- camera movement
- lighting
- duration
- rejection criteria

### 5. Review Loop

Every failed output becomes a rule.

Track:

- what failed
- why it failed
- which prompt repair worked
- whether the shot should be regenerated or cut

## Why This Transfers To A Second Song

You keep the engineering system and replace only:

- song analysis
- visual world
- asset references
- shot list

The production discipline stays the same.

