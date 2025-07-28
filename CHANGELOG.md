# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

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
