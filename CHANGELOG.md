# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

## [0.3.0](https://github.com/enzhao/Sentinel/compare/v0.2.0...v0.3.0) (2025-08-25)


### Features

* **backend:** add market monitor and tax configuration ([21b0040](https://github.com/enzhao/Sentinel/commit/21b004087f91fb653021af915fd0da6aabe00e29)), closes [#20](https://github.com/enzhao/Sentinel/issues/20)
* **data:** trigger background backfill on new holding ([ece6d10](https://github.com/enzhao/Sentinel/commit/ece6d10e28ca5ce1d7135774e6427de7e1d7f895)), closes [#4](https://github.com/enzhao/Sentinel/issues/4)
* **dev:** add script to generate mermaid diagrams from specs ([dbbca28](https://github.com/enzhao/Sentinel/commit/dbbca28f678ca602635a441c794a7fc39384c3d2)), closes [#4](https://github.com/enzhao/Sentinel/issues/4) [#8](https://github.com/enzhao/Sentinel/issues/8)
* **spec:** define strategy rule management and tax configuration ([2760a05](https://github.com/enzhao/Sentinel/commit/2760a0531182ec0acbdf0a7acbaf2e5c10af067d)), closes [#4](https://github.com/enzhao/Sentinel/issues/4)

## [0.2.0](https://github.com/enzhao/Sentinel/compare/v0.1.0...v0.2.0) (2025-07-31)


### Features

* **auth:** disable public user signup ([35bc64a](https://github.com/enzhao/Sentinel/commit/35bc64a1ac3f5a14f8b905cc60e0c312082f8835)), closes [#4](https://github.com/enzhao/Sentinel/issues/4)
* **backend:** calculate all technical indicators internally ([4b1ac9c](https://github.com/enzhao/Sentinel/commit/4b1ac9c04d19ff20960d4e29219f04bf9599cb2e)), closes [#4](https://github.com/enzhao/Sentinel/issues/4)
* **data:** expand market data model with VWMA ([161ec97](https://github.com/enzhao/Sentinel/commit/161ec976fa4514bcc5027788c9a482e005289481)), closes [#4](https://github.com/enzhao/Sentinel/issues/4)
* **frontend:** refactor UI to vuetify and update tests ([989a5b3](https://github.com/enzhao/Sentinel/commit/989a5b3d785ab2fe3db7f792be29b7f44c4ddafc)), closes [#4](https://github.com/enzhao/Sentinel/issues/4)
* **spec:** add MACD indicator and clarify VWMA calculation ([9550bef](https://github.com/enzhao/Sentinel/commit/9550bef915c7d33cd2f9dc5939126e67039ee35d)), closes [#4](https://github.com/enzhao/Sentinel/issues/4)


### Bug Fixes

* **api:** use REST convention for user creation. [#4](https://github.com/enzhao/Sentinel/issues/4) ([72499ee](https://github.com/enzhao/Sentinel/commit/72499ee70eb5458cc4429393e6020817357cfe65))
* **backend:** add expireAt to make TTL configurable in GC Firestore. [#4](https://github.com/enzhao/Sentinel/issues/4) ([6b7bad8](https://github.com/enzhao/Sentinel/commit/6b7bad8ef40b7d3a38e685c57d8509a0cd0af104))
* **deps:** regenerate requirements.txt to fix Docker build ([b6f60f9](https://github.com/enzhao/Sentinel/commit/b6f60f95a10abbe02e7572b699cf26326352236e)), closes [#4](https://github.com/enzhao/Sentinel/issues/4)
* **firebase:** proxy api requests to cloud run ([1ddac9d](https://github.com/enzhao/Sentinel/commit/1ddac9dedce554fbf03f54b2a2cb59db538a5f13)), closes [#4](https://github.com/enzhao/Sentinel/issues/4)
* **frontend:** correct auth state mocking in tests ([de4e9b1](https://github.com/enzhao/Sentinel/commit/de4e9b1b8cbf9cea8a65c17ae89d46a6402d986e)), closes [#4](https://github.com/enzhao/Sentinel/issues/4)
* **signup:** add idempotencyKey handling and fix the API, also the frontend  [#4](https://github.com/enzhao/Sentinel/issues/4) ([04e0247](https://github.com/enzhao/Sentinel/commit/04e0247f21221742db8f7fc588d596502cf14de5))

## [0.1.0](https://github.com/enzhao/Sentinel/compare/v0.0.0...v0.1.0) (2025-07-28)


### Features

* **api:** enforce UUID v4 for idempotency keys ([bebf2d2](https://github.com/enzhao/Sentinel/commit/bebf2d2ffc46c313fd8c5f8c545765ccf4d8e514)), closes [#14](https://github.com/enzhao/Sentinel/issues/14)
* **ci:** add a manual job to automate release. [#7](https://github.com/enzhao/Sentinel/issues/7) ([708531d](https://github.com/enzhao/Sentinel/commit/708531db88f530997f6566a10f319f1a1f288411))
* **data:** implement full market data sync and backfill ([1f4b3b7](https://github.com/enzhao/Sentinel/commit/1f4b3b7ec50f4b4176364d101f988d5bf8371792)), closes [#15](https://github.com/enzhao/Sentinel/issues/15)
* **data:** implement Market Data Caching and Historical Backfill ([6f26eaf](https://github.com/enzhao/Sentinel/commit/6f26eafedfd7d26c3c72c497560d1783612ed400)), closes [#15](https://github.com/enzhao/Sentinel/issues/15)
* **system:** add testing framework and enrich portfolio data ([e882a8b](https://github.com/enzhao/Sentinel/commit/e882a8b53efab585b22315112b1dcdc362820397)), closes [#4](https://github.com/enzhao/Sentinel/issues/4) [#5](https://github.com/enzhao/Sentinel/issues/5) [#6](https://github.com/enzhao/Sentinel/issues/6) [#9](https://github.com/enzhao/Sentinel/issues/9) [#10](https://github.com/enzhao/Sentinel/issues/10) [#11](https://github.com/enzhao/Sentinel/issues/11) [#12](https://github.com/enzhao/Sentinel/issues/12) [#13](https://github.com/enzhao/Sentinel/issues/13)


### Bug Fixes

* **api:** add format uuid for the idempotency keys. Backend: Idempotency Key should be UUID 4 ([a27a498](https://github.com/enzhao/Sentinel/commit/a27a49822acfa1b964fb6867921e5f7235053172)), closes [#14](https://github.com/enzhao/Sentinel/issues/14)
* **ci:** generate requirements files in workflow ([8e937cc](https://github.com/enzhao/Sentinel/commit/8e937cc5a3c335ce2d6e73afa409a8e3f157855c))

## 0.0.0 (2025-07-27)


### Features

* **auth, docs:** Implement user authentication and refactor spec ([56626ce](https://github.com/enzhao/Sentinel/commit/56626ce5e782e4f0fd60f1f67b905f470cbe89aa)), closes [#3](https://github.com/enzhao/Sentinel/issues/3)
* **dx:** implement conventional commits and release automation ([5c33f25](https://github.com/enzhao/Sentinel/commit/5c33f253fdba5f023eded4f3dbce9c4e53afc77b)), closes [#7](https://github.com/enzhao/Sentinel/issues/7)
* Implement initial CI/CD pipeline. Ref: [#1](https://github.com/enzhao/Sentinel/issues/1) ([4a15352](https://github.com/enzhao/Sentinel/commit/4a1535245cbe7f0f30e40741450ef56963d956ec))
