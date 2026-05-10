# Digital Archive — Text Cleanliness Report

*Generated 2026-05-10 from `logs/reports/final_validation.json`, `logs/reports/corpus_audit_report.json`, `logs/passage_subsequence_proof.json`, and `01_library/library/metadata/registry.json`. This is a reporting artifact — no corpus content has been touched.*

---

## 1. Short conclusion

**Passage integrity is very strong. The vast majority of "needs work" texts are not corrupted.**

Of the 1,091 distinct texts in the canonical library, every passage that the reader sees has been verified — at 99.88% overall — as a verbatim substring of its named raw source. **Zero texts** currently fail the 95 % integrity threshold.

"Needs work" almost always means one of three things, in decreasing order of frequency:

- the parser produced **duplicate passage ids** because it did not see the work's book / section structure (verse 1 of every book collides at id `1.1`);
- the parser left **heading-like lines inside the body** ("BOOK I" appearing as a passage rather than as a structural marker);
- the text has **many very short passages** that are likely speaker labels, separators, or OCR fragments rather than legitimate verses.

These are formatting and navigation issues, not preservation issues. The text is intact in raw form; the reader's view is imperfect but the words are right.

---

## 2. Summary counts

| Measure | Value |
|---|---:|
| Distinct canonical texts | **1,091** |
| Translations published (web reader) | 1,200 |
| `text.json` files on disk | 1,131 |
| | |
| **Clean** | **666 (61.0%)** |
| **Acceptable** | **109** |
| **Needs work** | **316 (29.0%)** |
| | |
| Texts with parser duplicate-ID issues | 39 |
| Total residual duplicate passages | 12,756 |
| Quality flags raised | 551 |
| Schema warnings (mostly metadata gaps) | 233 |
| | |
| Overall passage integrity | **99.88%** |
| Translations at 100% verified | 706 |
| Translations at <95% verified | **0** |

---

## 3. How to read the lists below

- Texts are grouped by tradition, sorted by tradition size.
- Each line shows the canonical id and the title.
- For *needs work* and *acceptable*, the line shows the primary issue counts in italics.
- Definitions for *clean* / *acceptable* / *needs work* are in §9.
- The lists below count distinct canonical works (`text.json` records in `registry.json`), not the 1,200 published translations.

---

## 4. Clean texts (666)

Schema-valid, no duplicate-id collisions, no significant heading leakage. Reader-facing structure matches the source's structure.

### Modern Philosophy (142)

- `a-dreamers-tales-lord-dunsany-1910` — A Dreamer's Tales
- `a-dweller-on-two-planets-frederick-oliver-189` — A Dweller on Two Planets
- `freud-psychoanalysis` — A General Introduction to Psychoanalysis
- `berkeley-principles` — A Treatise Concerning the Principles of Human Knowledge
- `a-very-pleasaunt-fruitful-diologe-called-the-epicur-erasmus` — A Very Pleasaunt & Fruitful Diologe Called the Epicur
- `locke-essay-vol1` — An Essay Concerning Human Understanding, Vol. 1
- `berkeley-vision` — An Essay Towards a New Theory of Vision
- `atlantida-pierre-benoit-1920` — Atlantida
- `mill-autobiography` — Autobiography
- `beyond-good-and-evil` — Beyond Good and Evil
- `book-of-knowledge-oahspe` — Book of Knowledge__(Oahspe)
- `buddhas-life-a-ferdinand-herold-t` — Buddha's Life
- `bushido-the-soul-of-japan-inazo-nitobe-1905` — Bushido - the Soul of Japan
- `carmina-gadelica-vol-2-alexander-carmicheal` — Carmina Gadelica - Vol 2
- `cerberus-the-dog-of-hades-the-history-of-maurice-bloomfield` — Cerberus the dog of Hades - The history of an idea
- `peirce-chance-love-logic` — Chance, Love, and Logic
- `code-of-the-illuminati-part-iii-of-memoirs-robert-clifford-1` — Code of the Illuminati Part III of Memoirs Illustrating the History of Jacobinism - A Barruel
- `schopenhauer-counsels-maxims` — Counsels and Maxims
- `kant-critique-judgement` — Critique of Judgement
- `hume-dialogues-religion` — Dialogues Concerning Natural Religion
- `lyttelton-dialogues-dead` — Dialogues of the Dead
- `frege-foundations-arithmetic` — Die Grundlagen der Arithmetik
- `die-wahlverwandtschaften-jo` — Die Wahlverwandtschaften
- `descartes-method` — Discourse on the Method
- `emile-jean-jacques-roussea` — Emile
- `rousseau-emile` — Emile, or On Education
- `essays-chance-love-logic-charles-peirce` — Essays - Chance Love & Logic
- `essays-the-will-to-believe-william-james` — Essays - The Will to Believe
- `james-radical-empiricism` — Essays in Radical Empiricism
- `bacon-essays` — Essays of Francis Bacon
- `emerson-essays-first` — Essays, First Series
- `schopenhauer-religion-dialogue` — Essays: Religion, A Dialogue, etc.
- `schopenhauer-controversy` — Essays: The Art of Controversy and Other Essays
- `faust-der-trag-die-erster-teil-johann-goethe` — Faust - Der Tragödie erster Teil
- `faust-in-original-metres-part-1-johann-goethe` — Faust - in Original Metres - Part 1
- `goethe-faust` — Faust: A Tragedy
- `kierkegaard-fear-trembling` — Fear and Trembling
- `fifty-one-tales-lord-dunsany-1915` — Fifty-one Tales
- `folk-lore-of-the-holy-land-moslem-christian-je-hanauer-1907` — Folk-lore of the Holy Land - Moslem Christian & Jewish
- `foxglove-and-some-of-its-medical-uses-william-withering` — Foxglove and some of its Medical Uses
- `kant-fundamental-principles` — Fundamental Principles of the Metaphysic of Morals
- `genji-monogatari-lady-murasaki-shikibu-suematsu-kencho-1900` — Genji Monogatari - Lady Murasaki Shikibu
- `giordano-bruno` — Giordano Bruno
- `gleaings-in-buddha-fields-lafcadio-hearn-1897` — Gleaings in Buddha-Fields
- `human-all-too-human` — Human, All Too Human
- `hypatia-john-toland` — Hypatia
- `kung-fu-tauist-medical-gymnastics-john-dudgeon-1895` — Kung-Fu - Tauist Medical Gymnastics
- `latin-vulgate-esther-liber-esther-anonymous` — Latin Vulgate - Esther (Liber Esther)
- `hegel-lectures-history-vol1` — Lectures on the History of Philosophy, Vol 1
- `hegel-lectures-history-vol3` — Lectures on the History of Philosophy, Vol 3
- `lives-vol-1-plutarch` — Lives - Vol 1
- `lives-vol-2-plutarch` — Lives - Vol 2
- `lives-vol-3-plutarch` — Lives - Vol 3
- `lives-vol-4-plutarch` — Lives - Vol 4
- `goethe-maxims` — Maxims and Reflections
- `mazes-and-labyriths-wh-matthews-1922` — Mazes and Labyriths
- `descartes-meditations` — Meditations on First Philosophy
- `mental-radio-upton-sinclair-1930` — Mental Radio
- `midrash-tanuma-no` — Midrash Tanuma
- `leibniz-monadology` — Monadology
- `montaignes-travels-in-italy-by-way-of-switzerland-montaigne` — Montaigne's travels in Italy by way of Switzerland and Germany in 1580 & 1581 - Vol 3
- `montaigne-travels-vol1` — Montaigne's Travels in Italy, Vol 1
- `montaigne-travels-vol2` — Montaigne's Travels in Italy, Vol 2
- `montaigne-travels-vol3` — Montaigne's Travels in Italy, Vol 3
- `morals-plutarch` — Morals
- `russell-mysticism-logic` — Mysticism and Logic and Other Essays
- `emerson-nature` — Nature
- `nostradamus-nostradamus` — Nostradamus
- `bacon-novum-organum` — Novum Organum
- `on-airs-waters-and-places-hippocrates` — On Airs Waters and Places
- `schopenhauer-sufficient-reason` — On the Fourfold Root of the Principle of Sufficient Reason
- `spinoza-improvement` — On the Improvement of the Understanding
- `darwin-origin-species` — On the Origin of Species
- `russell-external-world` — Our Knowledge of the External World
- `kant-perpetual-peace` — Perpetual Peace
- `moore-philosophical-studies` — Philosophical Studies
- `poems-edgar-allan-poe` — Poems
- `poems-ralph-emerson` — Poems
- `poems-robert-frost` — Poems
- `poems-of-american-patriotism-brander-matthews` — Poems of American Patriotism
- `poems-1-jonathan-swift` — Poems(1)
- `poems-2-jonathan-swift` — Poems(2)
- `james-pragmatism-full` — Pragmatism: A New Name for Some Old Ways of Thinking
- `james-psychology-briefer` — Psychology: Briefer Course
- `rataplan-a-rogue-elephant-other-stories` — Rataplan a Rogue Elephant & Other Stories
- `sacred-books-of-the-east-sam-beal` — Sacred Books of the East
- `saddharma-pundarika-buddhism` — Saddharma-Pundarika
- `select-list-of-books-relating-to-the-far-appleton-griggin` — Select List of Books Relating to the Far East
- `selected-writings-kierkegaard` — Selected Writings
- `descartes-principles` — Selections from the Principles of Philosophy
- `selestors-men-of-atlantis-clara-iza-von-ravn-1` — Selestor's Men of Atlantis
- `stonehenge-a-temple-restord-to-the-british-druids-william-st` — Stonehenge - A Temple Restor'd to the British Druids
- `schopenhauer-studies-pessimism` — Studies in Pessimism
- `studies-in-religious-personality-harold-begbie` — Studies in Religious Personality
- `s-mmtliche-werke-8-vermischte-schriften-und-aufs-johann-fich` — Sämmtliche Werke 8 - Vermischte Schriften und Aufsätze
- `tales-of-wonder-lord-dunsany-1916` — Tales of Wonder
- `the-aeneid-virgil-tr-john-dryde` — The Aeneid
- `russell-analysis-mind` — The Analysis of Mind
- `nietzsche-antichrist` — The Antichrist
- `schopenhauer-art-literature` — The Art of Literature
- `the-bustan-of-sadi-a-hart-edwards-1911` — The Bustan of Sadi
- `the-colloquies-of-erasmus-vol-1-erasmus` — The Colloquies of Erasmus - Vol 1
- `rousseau-confessions` — The Confessions
- `russell-conquest-happiness` — The Conquest of Happiness
- `darwin-descent-man-vol1` — The Descent of Man, and Selection in Relation to Sex (Volume 1)
- `the-diwan-of-abul-ala-henry-baerlein-1909` — The Diwan of Abu'l-Ala
- `the-gateless-gate-mu-mon-ekai-tr-nyogen-senza` — The Gateless Gate (Mu-mon)
- `freud-interpretation-dreams` — The Interpretation of Dreams
- `nietzsche-joyful-wisdom` — The Joyful Wisdom
- `the-lost-continent-cutcliffe-hyne-1900` — The Lost Continent
- `james-meaning-truth` — The Meaning of Truth
- `kant-metaphysical-ethics` — The Metaphysical Elements of Ethics
- `rank-myth-hero-birth` — The Myth of the Birth of the Hero
- `engels-origin-family` — The Origin of the Family, Private Property, and the State
- `hegel-philosophy-fine-art-vol1` — The Philosophy of Fine Art, Vol 1
- `brett-gassendi` — The Philosophy of Gassendi
- `spinoza-philosophy-selections` — The Philosophy of Spinoza
- `russell-problems-philosophy` — The Problems of Philosophy
- `the-rubaiyat-omar-khayyam` — The Rubaiyat
- `kierkegaard-sickness-unto-death` — The Sickness Unto Death
- `the-siksha-patri-of-the-svami-narayana-sect-monier-williams` — The Siksha-Patri of the Svami-Narayana Sect
- `rousseau-social-contract-discourses` — The Social Contract & Discourses
- `mill-subjection-women` — The Subjection of Women
- `the-sutta-nipata-v-fausboll-1881-no` — The Sutta-Nipata
- `jung-theory-psychoanalysis` — The Theory of Psychoanalysis
- `james-varieties-religious` — The Varieties of Religious Experience
- `james-will-to-believe` — The Will to Believe and Other Essays
- `will-to-power-3-4` — The Will to Power, Books 3-4
- `nietzsche-will-to-power-3-4` — The Will to Power, Part 3 & 4
- `the-yoga-sutras-charles-johnson-1912` — The_Yoga_Sutras
- `leibniz-theodicy` — Theodicy
- `spinoza-theologico-1` — Theologico-Political Treatise, Part 1
- `berkeley-three-dialogues` — Three Dialogues Between Hylas and Philonous
- `santayana-three-poets` — Three Philosophical Poets
- `thrice-greatest-hermes-vol-1-grs-mead-1906` — Thrice-Greatest Hermes - Vol 1
- `wittgenstein-tractatus` — Tractatus Logico-Philosophicus
- `twilight-idols` — Twilight of the Idols
- `viettelij-n-p-iv-kirja-kierkegaard` — Viettelijän päiväkirja
- `thoreau-walden` — Walden, and On the Duty of Civil Disobedience
- `wissenschaft-der-logik-band-1-hegel` — Wissenschaft der Logik - Band 1
- `yajur-veda-black-arthur-keith-1914-no` — Yajur Veda (black)
- `diamond-sutra-kumarajiva` — 金剛般若波羅蜜經 (Diamond Sutra)

### Christian (64)

- `erasmus-dialoge-two-persons` — A Dialoge or Communication of Two Persons
- `cunningham-origen-celsus` — A Dissertation on Origen Against Celsus
- `newman-apologia` — Apologia pro vita sua
- `celsus-porphyry-julian-against-christians` — Arguments of Celsus, Porphyry, and Julian Against the Christians
- `barlaam-ioasaph` — Barlaam and Ioasaph
- `bible` — Bible
- `luther-galatians` — Commentary on the Epistle to the Galatians
- `confessiones-saint-augustine-lati` — Confessiones
- `augustine-confessions` — Confessions
- `cosmic-consciousness-bucke` — Cosmic Consciousness
- `deuterocanonical-books-of-the-bible-anonymous` — Deuterocanonical Books of the Bible
- `doctrine-covenants-lds` — Doctrine and Covenants
- `erasmus-war` — Erasmus Against War
- `besant-esoteric-christianity` — Esoteric Christianity
- `foxe-book-martyrs` — Foxe's Book of Martyrs
- `kingsley-hypatia` — Hypatia, or New Foes with an Old Face
- `erasmus-folly` — In Praise of Folly
- `in-tune-infinite-trine` — In Tune With the Infinite
- `calvin-institutes` — Institutes of the Christian Religion
- `alfred-augustine-soliloquies` — King Alfred's Old English Version of Augustine's Soliloquies
- `lake-landmarks-early-christianity` — Landmarks in the History of Early Christianity
- `latin-vulgate-bible-book-titles-names-anonymous` — Latin Vulgate - Bible Book Titles & Names
- `calvin-letters` — Letters of John Calvin
- `boehme-hartmann` — Life and Doctrines of Jacob Boehme
- `butler-lives-saints` — Lives of the Saints
- `mysticism-underhill` — Mysticism
- `oahspe-newbrough` — Oahspe: A New Bible
- `old-english-poems` — Old English Poems
- `valla-donation-constantine` — On the Donation of Constantine
- `erasmus-education-children` — On the Education of Children
- `chrysostom-priesthood` — On the Priesthood
- `albertus-union-with-god` — On Union with God
- `chesterton-orthodoxy` — Orthodoxy
- `pagan-regeneration-willoughby` — Pagan Regeneration
- `hippolytus-philosophumena` — Philosophumena
- `rossetti-poems` — Poems by Christina Rossetti
- `prayers-middle-ages` — Prayers of the Middle Ages
- `julian-revelations` — Revelations of Divine Love
- `athanasius-biography` — Saint Athanasius: the Father of Orthodoxy
- `bible-contradictions-burr` — Self-Contradictions of the Bible
- `blake-songs-innocence-experience` — Songs of Innocence and of Experience
- `the-amish-smith` — The Amish
- `gracian-worldly-wisdom` — The Art of Worldly Wisdom
- `biography-bible-goodspeed` — The Biography of the Bible
- `book-of-mormon` — The Book of Mormon
- `cloud-unknowing-underhill` — The Cloud of Unknowing
- `cloud-sanctuary-eckartshausen` — The Cloud Upon the Sanctuary
- `erasmus-colloquies-vol1` — The Colloquies of Erasmus, Vol 1
- `complete-sayings-jesus` — The Complete Sayings of Jesus
- `didache-riddle` — The Didache
- `dante-divine-comedy` — The Divine Comedy
- `dolorous-passion-emmerich` — The Dolorous Passion of Our Lord Jesus Christ
- `expositor-bible` — The Expositor's Bible
- `first-book-adam-eve` — The First Book of Adam and Eve
- `forgotten-books-eden` — The Forgotten Books of Eden
- `conybeare-historical-christ` — The Historical Christ
- `imitation-of-christ` — The Imitation of Christ
- `jefferson-bible` — The Life and Morals of Jesus of Nazareth
- `little-flowers-francis` — The Little Flowers of St. Francis
- `lost-books-bible` — The Lost Books of the Bible
- `luther-smalcald-articles` — The Smalcald Articles
- `spiritual-exercises-ignatius` — The Spiritual Exercises of St. Ignatius of Loyola
- `wanderings-manuscripts-james` — The Wanderings and Homes of Manuscripts
- `eliot-waste-land` — The Waste Land

### Greek Literature (55)

- `shakespeare-a-lovers-complaint` — A Lover’s Complaint
- `aeneid` — Aeneid
- `beowulf` — Beowulf
- `devil-stories-anthology` — Devil Stories: An Anthology
- `hesiod-works` — Hesiod, the Homeric Hymns, and Homerica
- `tacitus-histories` — Histories
- `history-of-herodotus-vol-1-herodotus` — History of Herodotus - Vol 1
- `history-of-herodotus-vol-2-herodotus` — History of Herodotus - Vol 2
- `iliad-of-homer-samuel-butler-1898` — Iliad of Homer
- `hippocrates-instruments-of-reduction` — Instruments of Reduction
- `shakespeare-loves-labours-lost` — Love’s Labour’s Lost
- `euripides-medea` — Medea
- `ovid-metamorphoses` — Metamorphoses
- `bacon-new-atlantis` — New Atlantis
- `odyssey` — Odyssey
- `oedipus-king-of-thebes-sophocles` — Oedipus King of Thebes
- `bacon-of-gardens` — Of Gardens (an essay)
- `paradise-lost` — Paradise Lost
- `sophocles-three-plays` — Plays of Sophocles: Oedipus Rex, Oedipus at Colonus, Antigone
- `plutarch-lives-vol1` — Plutarch's Lives, Volume 1
- `plutarch-lives-vol3` — Plutarch's Lives, Volume 3
- `plutarch-lives-vol4` — Plutarch's Lives, Volume 4
- `aeschylus-prometheus-seven` — Prometheus Bound and The Seven Against Thebes
- `bacon-advancement-learning` — The Advancement of Learning
- `aristophanes-birds` — The Birds
- `huxley-burning-wheel` — The Burning Wheel
- `aristophanes-clouds` — The Clouds
- `shakespeare-the-comedy-of-errors` — The Comedy of Errors
- `aristophanes-frogs` — The Frogs
- `herodotus-histories-vol1` — The Histories, Volume 1
- `herodotus-histories-vol2` — The Histories, Volume 2
- `herodotus-history-rawlinson` — The History of Herodotus (Rawlinson)
- `thucydides-peloponnesian-war` — The History of the Peloponnesian War
- `aeschylus-house-atreus` — The House of Atreus (Oresteia)
- `shakespeare-the-life-and-death-of-king` — The Life and Death of King Richard the Second
- `shakespeare-the-life-of-king-henry-the` — The Life of King Henry the Fifth
- `shakespeare-the-merchant-of-venice` — The Merchant of Venice
- `shakespeare-the-merry-wives-of-windsor` — The Merry Wives of Windsor
- `shakespeare-the-passionate-pilgrim` — The Passionate Pilgrim
- `shakespeare-the-phoenix-and-the-turtle` — The Phoenix and the Turtle
- `shakespeare-the-rape-of-lucrece` — The Rape of Lucrece
- `pater-renaissance` — The Renaissance: Studies in Art and Poetry
- `shakespeare-the-second-part-of-king-henry` — The Second Part of King Henry the Sixth
- `the-seven-plays-in-english-verse-sophocles` — The Seven Plays in English Verse
- `sophocles-seven-plays` — The Seven Plays of Sophocles
- `shakespeare-the-sonnets` — The Sonnets
- `shakespeare-the-third-part-of-king-henry` — The Third Part of King Henry the Sixth
- `euripides-tragedies-vol1` — The Tragedies of Euripides, Vol 1
- `shakespeare-the-tragedy-of-king-lear` — The Tragedy of King Lear
- `shakespeare-the-tragedy-of-titus-andronicus` — The Tragedy of Titus Andronicus
- `morris-well-worlds-end` — The Well at the World's End
- `arnold-phra-phoenician` — The Wonderful Adventures of Phra the Phoenician
- `morris-wood-beyond-world` — The Wood Beyond the World
- `bacon-valerius-terminus` — Valerius Terminus, of the Interpretation of Nature
- `shakespeare-venus-and-adonis` — Venus and Adonis

### Hindu (36)

- `gandhi-guide-health` — A Guide to Health
- `dasgupta-indian-philosophy` — A History of Indian Philosophy, Volume 1
- `besant-yoga` — An Introduction to Yoga
- `bhagavad-gita` — Bhagavad Gita
- `brahma-knowledge-barnett` — Brahma Knowledge
- `krishnamurti-education-service` — Education as Service
- `gitanjali-tagore` — Gitanjali
- `tagore-gitanjali` — Gitanjali (Song Offerings)
- `hindu-law-judicature-sastri` — Hindu Law and Judicature from the Dharma-Śāstra
- `hindu-mythology` — Hindu Mythology, Vedic and Puranic
- `tamil-saivite-hymns` — Hymns of the Tamil Saivite Saints
- `arnold-indian-poetry` — Indian Poetry
- `vivekananda-jnana-yoga` — Jñāna Yoga, Part 2
- `vivekananda-karma-yoga` — Karma-Yoga
- `mahabharata` — Mahabharata
- `mahabharata-of-krishna-dwaipayana-vyasa-vol-1-ganguli` — Mahabharata of Krishna-Dwaipayana Vyasa - Vol 1
- `mahabharata-of-krishna-dwaipayana-vyasa-vol-2-ganguli` — Mahabharata of Krishna-Dwaipayana Vyasa - Vol 2
- `mahabharata-of-krishna-dwaipayana-vyasa-vol-3-ganguli` — Mahabharata of Krishna-Dwaipayana Vyasa - Vol 3
- `mahabharata-of-krishna-dwaipayana-vyasa-vol-4-ganguli` — Mahabharata of Krishna-Dwaipayana Vyasa - Vol 4
- `tagore-nationalism` — Nationalism
- `tagore-sadhana` — Sadhana: The Realisation of Life
- `kabir-songs-tagore` — Songs of Kabir
- `tagore-stray-birds` — Stray Birds
- `tales-hindu-dramatists` — Tales from the Hindu Dramatists
- `atharva-veda-bloomfield` — The Atharva Veda (Hymns)
- `the-g-takam-l-garland-of-birth-stories-max-muller` — The Gâtakamâlâ (Garland of Birth-Stories)
- `hindu-astrology-seva` — The Hindu Book of Astrology
- `tagore-home-world` — The Home and the World
- `ramayana-dutt` — The Ramayana (Dutt)
- `sama-veda-griffith` — The Sama Veda
- `sanskrit-drama-keith` — The Sanskrit Drama
- `upanishads-johnson` — The Upanishads (Johnson)
- `yajur-veda-keith` — The Yajur Veda (Taittiriya Saṃhitā)
- `upanishads-30-minor-aiyar` — Thirty Minor Upanishads
- `vedic-hymns-part2` — Vedic Hymns, Part 2
- `yoga-philosophy-religion-dasgupta` — Yoga as Philosophy and Religion

### Greek Philosophy (46)

- `plotinus-essay-beautiful` — An Essay on the Beautiful
- `plato-apology` — Apology
- `aristarchus-copernicus-antiquity-heath` — Aristarchus of Samos: The Copernicus of Antiquity
- `athenian-constitution` — Athenian Constitution
- `aristotle-categories` — Categories
- `plato-charmides` — Charmides
- `plato-cratylus` — Cratylus
- `plato-critias` — Critias
- `plato-crito` — Crito
- `plato-eryxias` — Eryxias
- `plato-euthydemus` — Euthydemus
- `plato-euthyphro` — Euthyphro
- `plato-ion` — Ion
- `plato-laches` — Laches
- `plato-laws` — Laws
- `plato-lesser-hippias` — Lesser Hippias
- `plato-lysis` — Lysis
- `plato-menexenus` — Menexenus
- `plato-meno` — Meno
- `aristotle-metaphysics` — Metaphysics
- `nicomachean-ethics` — Nicomachean Ethics
- `ocellus-lucanus` — Ocellus Lucanus on the Nature of the Universe
- `hippocrates-airs-waters` — On Airs, Waters, and Places
- `hippocrates-ancient-medicine` — On Ancient Medicine
- `porphyry-on-images` — On Images
- `plato-parmenides` — Parmenides
- `plato-phaedo` — Phaedo
- `plato-phaedrus` — Phaedrus
- `plato-philebus` — Philebus
- `aristotle-physics` — Physics
- `plutarch-morals-theosophical-king` — Plutarch's Morals: Theosophical Essays
- `aristotle-poetics` — Poetics
- `plato-protagoras` — Protagoras
- `ptolemy-tetrabiblos-ashmand` — Ptolemy's Tetrabiblos
- `pythagoras-delphic-fairbanks` — Pythagoras and the Delphic Mysteries
- `aristotle-rhetoric` — Rhetoric
- `plato-seventh-letter` — Seventh Letter
- `plato-sophist` — Sophist
- `plato-statesman` — Statesman
- `plato-symposium` — Symposium
- `theophrastus-characters` — The Characters
- `the-enchiridion-epictetus` — The Enchiridion
- `epictetus-golden-sayings` — The Golden Sayings of Epictetus (with the Hymn of Cleanthes)
- `pythagoras-golden-verses-rowe` — The Golden Verses of Pythagoras
- `galileo-sidereal-messenger` — The Sidereal Messenger
- `plato-theaetetus` — Theaetetus

### Hermetic (32)

- `new-light-alchymie-sedziwoj` — A New Light of Alchymie
- `code-illuminati-barruel` — Code of the Illuminati (Barruel, Part III)
- `dragons-lore-ingersoll` — Dragons and Dragon Lore
- `symbolic-creatures-art-evans` — Fictitious and Symbolic Creatures in Art
- `gypsy-sorcery-leland` — Gypsy Sorcery and Fortune Telling
- `demonology-witchcraft-scott` — Letters on Demonology and Witchcraft
- `mazes-labyrinths-matthews` — Mazes and Labyrinths
- `moon-lore-harley` — Moon Lore
- `new-lands-fort` — New Lands
- `shamanism-siberia-czaplicka` — Shamanism in Siberia
- `symbolical-masonry-haywood` — Symbolical Masonry
- `book-talismans-pavitt` — The Book of Talismans, Amulets, and Zodiacal Gems
- `builders-newton` — The Builders
- `nostradamus-roberts` — The Complete Prophecies of Nostradamus
- `hermes-pymander` — The Divine Pymander
- `dore-lectures-troward` — The Dore Lectures on Mental Science
- `edinburgh-lectures-troward` — The Edinburgh Lectures on Mental Science
- `flying-saucers-keyhoe` — The Flying Saucers Are Real
- `history-devil-carus` — The History of the Devil and the Idea of Evil
- `kybalion-three-initiates` — The Kybalion
- `fechner-life-after-death` — The Little Book of Life After Death
- `lore-unicorn-shepard` — The Lore of the Unicorn
- `science-getting-rich-wattles` — The Science of Getting Rich
- `secret-science-miracles-long` — The Secret Science Behind Miracles
- `smoky-god-emerson` — The Smoky God
- `sorceress-michelet` — The Sorceress
- `treasure-atlantis-taine` — The Treasure of Atlantis
- `vampire-kith-kin-summers` — The Vampire: His Kith and Kin
- `thrice-greatest-hermes-vol1` — Thrice-Greatest Hermes, Vol 1
- `wild-talents-fort` — Wild Talents
- `with-adepts-hartmann` — With the Adepts: An Adventure Among the Rosicrucians
- `your-forces-larson` — Your Forces and How to Use Them

### Buddhist (47)

- `faxian-record` — A Record of Buddhistic Kingdoms
- `sutta-nipata-sujato` — Anthology of Discourses
- `buddhist-psalms` — Buddhist Psalms
- `patimokkha-tibetan` — Code of Discipline for Monks (Tibetan Mūlasarvāstivāda)
- `dhammapada` — Dhammapada
- `dialogues-buddha-rhys-davids` — Dialogues of the Buddha
- `katyayana-jayarava` — Discourse to Kātyāyana
- `eastern-stories` — Eastern Stories and Legends
- `tibetan-tantra-muses` — Esoteric Teachings of the Tibetan Tantra
- `suzuki-essays-zen` — Essays in Zen Buddhism (First Series)
- `gleanings-buddha-fields-hearn` — Gleanings in Buddha-Fields
- `udana-sujato` — Heartfelt Sayings
- `linked-discourses-sujato` — Linked Discourses
- `long-discourses-sujato` — Long Discourses
- `middle-discourses-sujato` — Middle Discourses
- `numbered-discourses-sujato` — Numbered Discourses
- `ordination-dharmaguptaka` — Ordination (Dharmaguptaka Vinaya Khandaka)
- `dipa-sutra-sujato` — Origination
- `pure-land-yamabe-sasaki` — Principal Teachings of the True Sect of Pure Land
- `therigatha-davids` — Psalms of the Sisters (Therīgāthā)
- `dhammapada-sujato` — Sayings of the Dhamma
- `she-rab-dong-bu-nagarjuna-tr-wl-camp` — She-rab Dong-bu
- `sherab-dongbu-campbell` — She-rab Dong-bu (The Prajñādaṇḍa)
- `itivuttaka-sujato` — So It Was Said
- `buddhas-life-olcott` — The Buddha's Life
- `nagara-sutra-sujato` — The City
- `creed-of-buddha` — The Creed of Buddha
- `lloyd-creed-half-japan` — The Creed of Half Japan
- `diamond-sutra` — The Diamond Sutra
- `arthaviniscaya-anandajoti` — The Discourse giving the Analysis of the Topics
- `pratityasamutpada-vaidya` — The Discourse giving the Explanation and Analysis of Conditional Origination from the Beginning
- `catusparisat-sutra-sujato` — The Discourse on the Fourfold Assembly
- `srona-sutra-sujato` — The Discourse to Śroṇa
- `arnold-essence-buddhism` — The Essence of Buddhism
- `gospel-of-buddha` — The Gospel of Buddha
- `jataka` — The Jātaka
- `garland-birth-stories-speyer` — The Jātakamālā: Garland of Birth-Stories
- `light-of-asia` — The Light of Asia
- `lotus-sutra-kern` — The Saddharma-Puṇḍarīka
- `thousand-buddhas-stein` — The Thousand Buddhas
- `vrksa-sutra-sujato` — The Tree
- `theravada-vinaya` — Theravāda Collection on Monastic Law
- `tibetan-folk-tales` — Tibetan Folk Tales
- `upayika-dhammadinna` — Upāyikā Fragments
- `theragatha-sujato` — Verses of the Senior Monks
- `therigatha-sujato` — Verses of the Senior Nuns
- `zen-for-americans-suzuki` — Zen for Americans

### Jewish (26)

- `josephus-against-apion` — Against Apion
- `abrahams-hebraic-bookland` — By-paths in Hebraic Bookland
- `abrahams-jewish-literature` — Chapters on Jewish Literature
- `duties-heart-bachya` — Duties of the Heart
- `folklore-holy-land-hanauer` — Folk-lore of the Holy Land: Moslem, Christian and Jewish
- `jewish-lit-essays-deutsch` — Jewish Literature and Other Essays
- `judaism-abrahams` — Judaism
- `lectures-on-the-history-of-philosophy-vol-3-hegel` — Lectures on the History of Philosophy - Vol 3
- `legends-babylon-egypt-king` — Legends of Babylon and Egypt in Relation to Hebrew Tradition
- `midrash-tanuma` — Midrash Tanhuma
- `old-testament-legends-james` — Old Testament Legends
- `philo-judaeus-conybeare` — Philo Judæus of Alexandria
- `midrash-tales-maxims-rapaport` — Tales and Maxims from the Midrash
- `book-of-delight-abrahams` — The Book of Delight and Other Papers
- `ginsburg-essenes` — The Essenes: Their History and Doctrines
- `golden-mountain-levin` — The Golden Mountain
- `ginsburg-kabbalah` — The Kabbalah
- `halevi-kuzari` — The Kuzari (Kitab al-Khazari)
- `ginzberg-legends-vol1` — The Legends of the Jews, Vol 1
- `ginzberg-legends-vol2` — The Legends of the Jews, Vol 2
- `ginzberg-legends-vol3` — The Legends of the Jews, Vol 3
- `ginzberg-legends-vol4` — The Legends of the Jews, Vol 4
- `josephus-life` — The Life of Flavius Josephus
- `the-philosophy-and-theology-averroes` — The Philosophy and Theology
- `tanakh` — The Tanakh
- `wisdom-talmud-bokser` — The Wisdom of the Talmud

### Political Philosophy (28)

- `vindication-rights-men` — A Vindication of the Rights of Men
- `engels-antiduehring` — Anti-Dühring
- `mill-representative-gov` — Considerations on Representative Government
- `machiavelli-discourses` — Discourses on Livy
- `feuerbach-engels` — Feuerbach
- `gandhi-freedoms-battle` — Freedom's Battle
- `machiavelli-florence` — History of Florence and of the Affairs of Italy
- `gandhi-indian-home-rule` — Indian Home Rule (Hind Swaraj)
- `machiavelli-plays` — La Mandragola, La Clizia, Belfagor
- `landmarks-of-scientific-socialism-anti-duehring-engels` — Landmarks of Scientific Socialism (Anti-Duehring)
- `hobbes-leviathan` — Leviathan
- `engels-feuerbach` — Ludwig Feuerbach and the End of Classical German Philosophy
- `machiavelli-vol1` — Machiavelli — Vol 1 (Selected Works)
- `on-liberty` — On Liberty
- `russell-political-ideals` — Political Ideals
- `russell-roads-freedom` — Proposed Roads to Freedom
- `locke-second-treatise` — Second Treatise of Government
- `engels-socialism-utopian` — Socialism: Utopian and Scientific
- `communist-manifesto` — The Communist Manifesto
- `engels-working-class` — The Condition of the Working-Class in England in 1844
- `english-utilitarians-stephen` — The English Utilitarians, Vol 1
- `russell-bolshevism` — The Practice and Theory of Bolshevism
- `the-prince` — The Prince
- `ambedkar-rupee` — The Problem of the Rupee
- `tocqueville-recollections` — The Recollections of Alexis de Tocqueville
- `roots-socialist-fortune` — The Roots of the Socialist Philosophy
- `wollstonecraft-education-daughters` — Thoughts on the Education of Daughters
- `utilitarianism` — Utilitarianism

### Celtic (26)

- `celtic-fairy-tales` — Celtic Fairy Tales
- `cuchulain-muirthemne-gregory` — Cuchulain of Muirthemne
- `feuds-clans-macgregor` — Feuds of the Clans
- `folk-tales-brittany-spence` — Folk Tales of Brittany
- `gypsy-folk-tales-groome` — Gypsy Folk Tales
- `legends-stories-ireland-lover` — Legends and Stories of Ireland
- `stonehenge-jones` — Stonehenge: A Temple Restor'd to the British Druids
- `lang-fairy-blue` — The Blue Fairy Book
- `lang-fairy-brown` — The Brown Fairy Book
- `candle-vision-ae` — The Candle of Vision
- `tain-cualnge-dunn` — The Cattle Raid of Cualnge (Táin Bó Cúalnge)
- `celtic-twilight-yeats` — The Celtic Twilight
- `lang-fairy-crimson` — The Crimson Fairy Book
- `fairy-faith-evans-wentz` — The Fairy-Faith in Celtic Countries
- `lang-fairy-green` — The Green Fairy Book
- `lang-fairy-grey` — The Grey Fairy Book
- `lang-fairy-lilac` — The Lilac Fairy Book
- `mabinogion-guest` — The Mabinogion
- `lang-fairy-olive` — The Olive Fairy Book
- `lang-fairy-orange` — The Orange Fairy Book
- `lang-fairy-pink` — The Pink Fairy Book
- `lang-fairy-red` — The Red Fairy Book
- `sacred-tree-philpot` — The Sacred Tree
- `lang-fairy-violet` — The Violet Fairy Book
- `lang-fairy-yellow` — The Yellow Fairy Book
- `true-irish-ghost-stories-seymour` — True Irish Ghost Stories

### Mesoamerican (23)

- `journey-siberia-curtin` — A Journey in Southern Siberia
- `apu-ollantay-markham` — Apu Ollantay
- `diegueno-waterman` — Ceremonies and Traditions of the Diegueño Indians
- `creation-myths-america` — Creation Myths of Primitive America
- `dancing-gods-fergusson` — Dancing Gods
- `hawaiian-folk-tales-thrum` — Hawaiian Folk Tales
- `indian-why-linderman` — Indian Why Stories
- `iroquoian-cosmology-hewitt` — Iroquoian Cosmology
- `maui-legends-westervelt` — Legends of Ma-ui, a Demi-God of Polynesia
- `own-land-myths-skinner` — Myths and Legends of Our Own Land
- `old-indian-legends-zitkala` — Old Indian Legends
- `rig-veda-americanus-brinton` — Rig Veda Americanus
- `spider-woman-reichard` — Spider Woman
- `nam-tales-thompson` — Tales of the North American Indians
- `incas-peru-markham` — The Incas of Peru
- `path-rainbow-cronyn` — The Path on the Rainbow
- `popol-vuh-spence` — The Popol Vuh
- `soul-indian-eastman` — The Soul of the Indian
- `thunderbird-tootooch-kirk` — The Thunder Bird Tootooch Legends
- `traditions-hopi-voth` — The Traditions of the Hopi
- `unwritten-hawaii-emerson` — Unwritten Literature of Hawaii
- `womans-mysteries-briffault` — Woman's Mysteries of a Primitive People
- `yana-texts-sapir` — Yana Texts

### Islam (16)

- `avicenna-soul` — A Compendium on the Soul
- `arabian-wisdom-wortabet` — Arabian Wisdom
- `salaman-absal-fitzgerald` — Salámán and Absál
- `afghan-poetry-dorn` — Selections from the Poetry of the Afghans
- `arab-conquests-central-asia-gibb` — The Arab Conquests in Central Asia
- `bustan-sadi-edwards` — The Bustan of Sa'di
- `ghazzali-confessions` — The Confessions of Al-Ghazzali
- `diwan-abu-al-ala-nicholson` — The Diwan of Abu'l-ʿAla al-Maʿarri
- `diwan-zeb-un-nissa-westbrook` — The Diwan of Zeb-un-Nissa
- `rumi-divan-festival` — The Festival of Spring
- `hujviri-kashf` — The Kashf al-Mahjub
- `love-letters-rumi` — The Love Letters
- `nicholson-mystics-islam` — The Mystics of Islam
- `persian-mystics-rumi` — The Persian Mystics: Jalalu'd-din Rumi
- `secret-rose-garden-shabistari` — The Secret Rose Garden
- `iqbal-secrets-of-self` — The Secrets of the Self (Asrār-i Khudī)

### Egyptian (20)

- `ancient-egyptian-legends` — Ancient Egyptian Legends
- `budge-egyptian-future` — Egyptian Ideas of the Future Life
- `egyptian-tales-1st-petrie` — Egyptian Tales (1st series)
- `egyptian-tales-2nd-petrie` — Egyptian Tales (2nd series)
- `maspero-history-egypt-vol1` — History of Egypt, Chaldea, Syria, Babylonia and Assyria, Vol 1
- `maspero-history-egypt-vol3` — History of Egypt, Chaldea, Syria, Babylonia and Assyria, Vol 3
- `maspero-history-egypt-vol4` — History of Egypt, Chaldea, Syria, Babylonia and Assyria, Vol 4
- `maspero-history-egypt-vol5` — History of Egypt, Chaldea, Syria, Babylonia and Assyria, Vol 5
- `maspero-history-egypt-vol6` — History of Egypt, Chaldea, Syria, Babylonia and Assyria, Vol 6
- `maspero-history-egypt-vol7` — History of Egypt, Chaldea, Syria, Babylonia and Assyria, Vol 7
- `maspero-history-egypt-vol8` — History of Egypt, Chaldea, Syria, Babylonia and Assyria, Vol 8
- `maspero-history-egypt-vol9` — History of Egypt, Chaldea, Syria, Babylonia and Assyria, Vol 9
- `records-of-the-past-2nd-series-vol-i-ah-sayce-1888` — Records of the Past - 2nd series - Vol I
- `records-of-the-past-2nd-series-vol-ii-ah-sayce-1888` — Records of the Past - 2nd series - Vol II
- `the-book-of-the-dead-wallis-budge` — The Book of the Dead
- `reisner-immortality` — The Egyptian Conception of Immortality
- `house-hidden-places-marsham` — The House of the Hidden Places
- `literature-ancient-egyptians-budge` — The Literature of the Ancient Egyptians
- `religion-egypt-petrie` — The Religion of Ancient Egypt
- `rosetta-stone-budge` — The Rosetta Stone

### Mesopotamian (19)

- `history-babylon-king` — A History of Babylon, from the Foundation of the Monarchy to the Persian Conquest
- `history-sumer-akkad-king` — A History of Sumer and Akkad
- `ancient-egypt-george-rawlinson-art` — Ancient Egypt
- `history-of-egypt-chaldea-syria-babylonia-assyria-lwking` — History of Egypt & Chaldea & Syria & Babylonia & Assyria
- `history-phoenicia-rawlinson` — History of Phoenicia
- `myths-babylonia-mackenzie` — Myths of Babylonia and Assyria
- `plutarchs-morals-theosophical-essays-charles-king-1908` — Plutarch's Morals Theosophical Essays
- `records-past-vol1` — Records of the Past, 2nd Series Vol 1
- `records-past-vol2` — Records of the Past, 2nd Series Vol 2
- `records-past-vol3` — Records of the Past, 2nd Series Vol 3
- `babylonian-creation-king` — The Babylonian Legends of Creation
- `budge-babylonian-deluge` — The Babylonian Story of the Deluge
- `gilgamesh-langdon` — The Epic of Gilgamesh
- `philistines-macalister` — The Philistines: Their History and Civilization
- `religion-babylonia-assyria-jastrow` — The Religion of Babylonia and Assyria
- `rawlinson-monarchy-vol2` — The Seven Great Monarchies, Vol 2: Assyria
- `rawlinson-monarchy-vol3` — The Seven Great Monarchies, Vol 3: Media
- `rawlinson-monarchy-vol4` — The Seven Great Monarchies, Vol 4: Babylon
- `seven-tablets-king` — The Seven Tablets of Creation

### Roman Philosophy (14)

- `cicero-brutus` — Brutus, or History of Famous Orators
- `tacitus-germania-agricola` — Germania and Agricola
- `cicero-letters-atticus-vol1` — Letters to Atticus, Vol 1
- `cicero-letters-atticus-vol2` — Letters to Atticus, Vol 2
- `cicero-letters-atticus-vol3` — Letters to Atticus, Vol 3
- `cicero-de-amicitia` — On Friendship & Scipio's Dream
- `lucretius-nature-things` — On the Nature of Things
- `pliny-natural-history-vol2` — The Natural History of Pliny, Vol 2
- `pliny-natural-history-vol3` — The Natural History of Pliny, Vol 3
- `pliny-natural-history-vol5` — The Natural History of Pliny, Vol 5
- `tacitus-reign-tiberius` — The Reign of Tiberius (Tacitus)
- `cicero-republic` — The Republic (De Re Publica)
- `the-tragedies-seneca` — The Tragedies
- `cicero-friendship-old-age` — Treatises on Friendship and Old Age

### Confucian (15)

- `more-translations-chinese-waley` — More Translations from the Chinese
- `analects` — The Analects
- `book-of-filial-duty` — The Book of Filial Duty (Hsiao Ching)
- `book-of-odes-jennings` — The Book of Odes (Shi Jing, Jennings)
- `chinese-classics-vol1-legge` — The Chinese Classics, Vol 1
- `chinese-fairy-book-wilhelm` — The Chinese Fairy Book
- `civilization-china-giles` — The Civilization of China
- `analects-legge-1893` — The Confucian Analects (Legge)
- `confucian-canon-bilingual` — The Confucian Canon (Chinese and English)
- `doctrine-of-the-mean` — The Doctrine of the Mean
- `great-learning` — The Great Learning
- `li-po-waley` — The Poet Li Po, AD 701-762
- `religions-ancient-china-giles` — The Religions of Ancient China
- `sayings-confucius-lyall` — The Sayings of Confucius
- `mencius` — The Works of Mencius

### Greek (11)

- `bloomfield-cerberus` — Cerberus, the Dog of Hades
- `euripides-and-his-age-murray` — Euripides and His Age
- `fairy-tales-greece` — Fairy Tales of Modern Greece
- `greek-popular-religion-nilsson` — Greek Popular Religion
- `hesiodi-carmina-latin-hesiod` — Hesiodi Carmina (Latin)
- `myths-crete-mackenzie` — Myths of Crete and Pre-Hellenic Europe
- `migration-fables-muller` — On the Migration of Fables
- `roman-greek-questions-plutarch` — Plutarch's Roman and Greek Questions
- `book-wonder-dunsany` — The Book of Wonder
- `evil-eye-elworthy` — The Evil Eye
- `gods-pegana-dunsany` — The Gods of Pegāna

### Taoist (9)

- `feng-shui-eitel` — Feng Shui
- `lao-tzu-sayings-lionel-giles-1905` — Lao-Tzu sayings
- `laotzu-goddard` — Laotzu's Tao & Wu Wei
- `myths-legends-china-werner` — Myths and Legends of China
- `sacred-places-china-edkins` — Sacred Places in China
- `tao-te-ching` — Tao Te Ching
- `laotzu-sayings-lionel-giles` — The Sayings of Lao Tzu
- `tao-teh-king-medhurst` — The Tao Teh King (Medhurst)
- `zhuangzi` — Zhuangzi

### Norse (7)

- `icelandic-sagas-vol3-dasent` — Icelandic Sagas, Vol 3
- `russian-tales-ransome` — Old Peter's Russian Tales
- `roumanian-fairy-kremnitz` — Roumanian Fairy Tales and Legends
- `slavonic-folktales-wratislaw` — Sixty Folk-Tales from Exclusively Slavonic Sources
- `teutonic-myth-guerber` — Teutonic Myth and Legend
- `oera-linda-sandbach` — The Oera Linda Book
- `poetic-edda` — The Poetic Edda

### Gnostic (6)

- `gospel-of-thomas` — Gospel of Thomas
- `apocryphon-of-john` — The Apocryphon of John
- `gospel-of-mary` — The Gospel of Mary
- `gospel-of-philip` — The Gospel of Philip
- `gospel-of-thomas-various` — The Gospel of Thomas
- `gospel-of-truth` — The Gospel of Truth

### Theosophy (2)

- `caves-jungles-hindostan-blavatsky` — From the Caves and Jungles of Hindostan
- `key-to-theosophy-blavatsky` — The Key to Theosophy

### Shinto (5)

- `hyakunin-isshu-porter` — A Hundred Verses from Old Japan
- `folk-tales-japan` — Ancient Tales and Folk-lore of Japan
- `japan-folklore-smith` — Ancient Tales and Folklore of Japan
- `pillow-book-sei-shonagon` — The Pillow-Book of Sei Shōnagon
- `genji-monogatari-suematsu` — The Tale of Genji (Abridged)

### Persian Literature (4)

- `gulistan-sadi` — The Gulistan
- `rawlinson-monarchy-vol5` — The Seven Great Monarchies, Vol 5: Persia
- `rawlinson-monarchy-vol6` — The Seven Great Monarchies, Vol 6: Parthia
- `rawlinson-monarchy-vol7` — The Seven Great Monarchies, Vol 7: The Sassanian (New Persian) Empire

### Stoic (5)

- `epictetus-discourses` — Discourses (Selections)
- `enchiridion` — Enchiridion
- `meditations` — Meditations
- `seneca-minor-dialogues` — Minor Dialogues and On Clemency
- `seneca-morals` — Of a Happy Life, Benefits, Anger, and Clemency

### (none) (1)

- `hesse-siddhartha` — hesse-siddhartha

### Sikh (1)

- `sikh-religion-vol6-macauliffe` — The Sikh Religion, Volume 6

### Slavic (2)

- `folk-tales-russian` — Folk Tales From the Russian
- `georgian-folk-tales` — Georgian Folk Tales

### Tibetan Buddhist (1)

- `bardo-thodol-evans-wentz` — The Tibetan Book of the Dead (Bardo Thödol)

### Japanese Philosophy (1)

- `bushido` — Bushido: The Soul of Japan

### Finnish (1)

- `kalevala` — The Kalevala

### Mohist (1)

- `mozi` — Mozi

---

## 5. Acceptable texts (109)

Minor issues — small heading leakage, uneven segment sizes, or many short passages — but readable end-to-end. *Acceptable* means the text is usable today; perfecting it is editorial work, not rescue work.

### Modern Philosophy (27)

- `james-pluralistic-universe` — A Pluralistic Universe — *3 heading leaks*
- `atharva-veda-hymns-ralph-griffith-1895` — Atharva Veda hymns — *3 heading leaks, 195 short*
- `spinoza-ethics` — Ethics — *5 heading leaks*
- `kundalini-the-mother-of-the-universe-rishi-singh-gherwal` — Kundalini - The Mother of the Universe — *4 heading leaks*
- `hegel-lectures-history-vol2` — Lectures on the History of Philosophy, Vol 2 — *3 heading leaks*
- `schopenhauer-basis-morality` — On the Basis of Morality — *3 heading leaks*
- `oracles-of-nostradamus-charles-ward-1891` — Oracles of Nostradamus — *3 heading leaks, 175 short*
- `hegel-philosophy-mind` — Philosophy of Mind — *5 heading leaks, 118 short*
- `plays-of-gods-and-men-lord-dunsany-1917` — Plays of Gods and Men — *4 heading leaks, 1,172 short*
- `plotinos-complete-works-vol-3-plotinos` — Plotinos - Complete Works - Vol 3 — *5 heading leaks, 201 short*
- `poems-victor-hugo` — Poems — *3 heading leaks, 191 short*
- `poems-by-emily-dickinso-emily-dickinson` — Poems by Emily Dickinso — *4 heading leaks, 671 short*
- `jung-psychology-unconscious` — Psychology of the Unconscious — *3 heading leaks, 1,066 short*
- `emerson-representative-men` — Representative Men — *1 dup ids*
- `tales-from-chaucer-charles-clarke-1833` — Tales from Chaucer — *3 heading leaks*
- `the-baltimore-catchecism-1891` — The Baltimore Catchecism — *3 heading leaks, 138 short*
- `dawn-of-day` — The Dawn of Day — *5 heading leaks*
- `hegel-philosophy-fine-art-vol2` — The Philosophy of Fine Art, Vol 2 — *4 heading leaks*
- `hegel-philosophy-fine-art-vol3` — The Philosophy of Fine Art, Vol 3 — *5 heading leaks*
- `hegel-philosophy-fine-art-vol4` — The Philosophy of Fine Art, Vol 4 — *4 heading leaks*
- `james-principles-psychology-vol1` — The Principles of Psychology, Volume 1 — *5 heading leaks, 137 short*
- `james-principles-psychology-vol2` — The Principles of Psychology, Volume 2 — *5 heading leaks, 172 short*
- `the-sayings-of-the-jewish-fathers-pirke-avot-joseph-gorfinkl` — The Sayings of the Jewish Fathers (Pirke Avot) — *5 heading leaks*
- `will-to-power-1-2` — The Will to Power, Books 1-2 — *3 heading leaks*
- `nietzsche-will-to-power-1-2` — The Will to Power, Part 1 & 2 — *5 heading leaks, 491 short*
- `schopenhauer-wisdom-life` — The Wisdom of Life — *5 heading leaks*
- `yoga-vashisht-or-heaven-found-rishi-singh-gherwal` — Yoga Vashisht or Heaven Found — *3 heading leaks*

### Christian (12)

- `atlantis-the-antediluvian-world-ignatius-donnelly-18` — Atlantis - the Antediluvian World — *5 heading leaks*
- `boulting-four-pilgrims` — Four Pilgrims — *4 heading leaks*
- `chrysostom-homilies-acts-romans` — Homilies on Acts and Romans — *4 heading leaks, 240 short*
- `chrysostom-homilies-corinthians` — Homilies on First and Second Corinthians — *4 heading leaks, 358 short*
- `pageant-popes-farrow` — Pageant of the Popes — *3 heading leaks, 529 short*
- `ruysbroeck-adornment` — The Adornment of the Spiritual Marriage — *5 heading leaks*
- `baltimore-catechism` — The Baltimore Catechism — *3 heading leaks, 138 short*
- `augustine-city-of-god` — The City of God — *4 heading leaks*
- `boethius-consolation` — The Consolation of Philosophy — *5 heading leaks, 147 short*
- `feuerbach-essence-christianity` — The Essence of Christianity — *3 heading leaks*
- `charnock-works` — The Works of Stephen Charnock — *4 heading leaks*
- `apostolic-fathers` — The Writings of the Apostolic Fathers — *3 heading leaks, 331 short*

### Greek Literature (6)

- `plutarch-lives-vol2` — Plutarch's Lives, Volume 2 — *1 dup ids*
- `plutarch-romane-questions` — Romane Questions — *4 dup ids, 116 short*
- `euripides-bacchae` — The Bacchae — *3 heading leaks, 325 short*
- `the-buddhavam-sa-and-the-cariya-pit-aka-richard-morris-no` — The Buddhavaṃsa and the Cariyā-piṭaka — *5 heading leaks*
- `the-works-of-hsuntze-homer-dubs-1928` — The Works of Hsuntze — *4 heading leaks, 671 short*
- `shakespeare-twelfth-night-or-what-you-will` — Twelfth Night; or, What You Will — *4 heading leaks*

### Hindu (9)

- `avat-ras-annie-besant` — Avatâras — *4 heading leaks*
- `besant-avataras` — Avatāras — *4 heading leaks*
- `kundalini-gherwal` — Kundalini: The Mother of the Universe — *4 heading leaks*
- `occult-chemistry-annie-besant` — Occult Chemistry — *4 heading leaks*
- `shankara-select-works` — Select Works of Sri Sankaracharya — *3 heading leaks*
- `tagore-post-office` — The Post Office — *3 heading leaks*
- `yoga-sutras` — The Yoga Sutras of Patanjali — *3 heading leaks*
- `vishnu-purana` — Vishnu Purana — *4 dup ids*
- `yoga-vasishtha-gherwal` — Yoga Vasishtha, or Heaven Found — *3 heading leaks*

### Greek Philosophy (5)

- `burnet-early-greek` — Early Greek Philosophy — *5 heading leaks, 1,114 short*
- `plato-gorgias` — Gorgias — *3 heading leaks, 134 short*
- `plotinus-complete-vol2` — Plotinus: Complete Works, Vol 2 — *5 heading leaks, 157 short*
- `plotinus-complete-vol3` — Plotinus: Complete Works, Vol 3 — *5 heading leaks, 201 short*
- `the-discourses-of-epictetus-pe-matheson-1916` — The Discourses of Epictetus — *5 heading leaks, 255 short*

### Hermetic (11)

- `chinese-occultism-skinner` — Chinese Occultism — *3 heading leaks, 284 short*
- `fortune-telling-cards-mayo` — Fortune Telling by Cards — *5 heading leaks, 382 short*
- `morals-dogma-pike` — Morals and Dogma of the Ancient and Accepted Scottish Rite — *5 heading leaks, 178 short*
- `ouspensky-tertium-organum` — Tertium Organum — *3 heading leaks*
- `book-damned-fort` — The Book of the Damned — *3 heading leaks, 112 short*
- `master-key-haanel` — The Master Key System — *5 heading leaks, 110 short*
- `origin-pyramid-staniland-wake` — The Origin and Significance of the Great Pyramid — *4 heading leaks*
- `quimby-manuscripts` — The Quimby Manuscripts — *3 heading leaks, 114 short*
- `sacred-symbols-mu-churchward` — The Sacred Symbols of Mu — *4 heading leaks, 456 short*
- `secret-ages-collier` — The Secret of the Ages — *3 heading leaks, 140 short*
- `thrice-greatest-hermes-vol2` — Thrice-Greatest Hermes, Vol 2 — *4 heading leaks, 211 short*

### Buddhist (5)

- `chinese-buddhism-edkins` — Chinese Buddhism — *3 heading leaks, 167 short*
- `dharmaguptaka-beal` — Dharmaguptaka Monks' Code of Discipline — *3 heading leaks*
- `buddhavamsa-cariyapitaka` — The Buddhavaṃsa and the Cariyā-piṭaka — *5 heading leaks*
- `buddhist-catechism` — The Buddhist Catechism — *5 heading leaks*
- `zen-buddhism-art-suzuki` — Zen Buddhism and Its Relation to Art — *4 heading leaks*

### Jewish (2)

- `lectures-on-the-history-of-philosophy-vol-2-hegel` — Lectures on the History of Philosophy - Vol 2 — *3 heading leaks*
- `studies-judaism-schechter` — Studies in Judaism — *4 heading leaks, 146 short*

### Political Philosophy (2)

- `paine-common-sense` — Common Sense — *3 heading leaks*
- `stirner-ego-his-own` — The Ego and His Own — *3 heading leaks, 229 short*

### Celtic (3)

- `carmina-gadelica-vol1` — Carmina Gadelica, Vol 1 — *3 heading leaks, 257 short*
- `scottish-fairy-douglas` — Scottish Fairy and Folk Tales — *3 heading leaks, 137 short*
- `cornwall-traditions-vol2-bottrell` — Traditions and Hearthside Stories of West Cornwall, Vol 2 — *5 heading leaks*

### Mesoamerican (3)

- `fjort-folklore-dennett` — Notes on the Folklore of the Fjort — *4 heading leaks*
- `navaho-origin-myths-matthews` — Origin Myths of the Navaho Indians — *3 heading leaks, 288 short*
- `algonquin-legends-leland` — The Algonquin Legends of New England — *4 heading leaks, 131 short*

### Islam (2)

- `conference-of-the-birds` — The Conference of the Birds — *5 heading leaks, 219 short*
- `wollaston-religion-koran` — The Religion of the Koran — *5 heading leaks*

### Egyptian (2)

- `maspero-history-egypt-vol2` — History of Egypt, Chaldea, Syria, Babylonia and Assyria, Vol 2 — *3 heading leaks*
- `legends-gods-budge` — Legends of the Gods — *5 heading leaks*

### Mesopotamian (1)

- `rawlinson-monarchy-vol1` — The Seven Great Monarchies, Vol 1: Chaldaea — *4 heading leaks*

### Roman Philosophy (3)

- `cicero-de-officiis` — De Officiis (On Duties) — *4 heading leaks*
- `pliny-natural-history-vol1` — The Natural History of Pliny, Vol 1 — *3 heading leaks, 157 short*
- `cicero-tusculan` — Tusculan Disputations — *5 heading leaks*

### Confucian (3)

- `170-chinese-poems-waley` — A Hundred and Seventy Chinese Poems — *5 heading leaks*
- `shijing-legge` — The Book of Poetry (Shi Jing) — *4 heading leaks, 280 short*
- `shundai-zatsuwa-kyuso` — The Shundai Zatsuwa — *4 heading leaks, 146 short*

### Greek (3)

- `eleusinian-mysteries-taylor` — The Eleusinian and Bacchic Mysteries — *3 heading leaks, 214 short*
- `syrian-goddess-lucian` — The Syrian Goddess (De Dea Syria) — *4 heading leaks, 155 short*
- `time-gods-dunsany` — Time and the Gods — *4 heading leaks*

### Taoist (2)

- `chuang-tzu-mystic-edition` — Chuang Tzu: Mystic, Moralist, and Social Reformer — *3 heading leaks, 596 short*
- `strange-stories-chinese-studio-giles` — Strange Stories from a Chinese Studio — *4 heading leaks, 403 short*

### Norse (2)

- `norse-tales-popular-dasent` — Popular Tales from the Norse — *4 heading leaks, 149 short*
- `children-odin-colum` — The Children of Odin — *3 heading leaks*

### Gnostic (1)

- `pistis-sophia-mead` — Pistis Sophia — *3 heading leaks, 509 short*

### Shinto (1)

- `kojiki-chamberlain` — The Kojiki — *3 heading leaks, 1,075 short*

### Persian Literature (1)

- `rubaiyat-omar-khayyam` — The Rubaiyat of Omar Khayyam — *1 dup ids*

### (none) (1)

- `don-quixote` — Don Quixote — *5 heading leaks, 659 short*

### Chinese Strategy (1)

- `art-of-war` — The Art of War — *1 dup ids*

### Bahai (1)

- `kitab-i-aqdas` — The Kitáb-i-Aqdas (The Most Holy Book) — *5 heading leaks, 274 short*

---

## 6. Needs-work texts (316)

Grouped by the **primary** parser/structure issue. The text itself is in raw form; the reader's view will be uneven until the listed issue is addressed. Most fixes are per-text parser work, not content rewrites.

### Duplicate-ID (parser) (24)

*Parser produced colliding passage ids — usually because the work's book/chapter/verse hierarchy was flattened. Fix: re-ingest with the correct hierarchy parser. Passage content is intact.*

**Modern Philosophy** (4)
- `genealogy-of-morals` — The Genealogy of Morals — *97 dup ids, 3 heading leaks*
- `hume-treatise` — A Treatise of Human Nature — *27 dup ids, 4 heading leaks*
- `spinoza-theologico-2` — Theologico-Political Treatise, Part 2 — *16 dup ids, 6 heading leaks*
- `birth-of-tragedy` — The Birth of Tragedy — *18 dup ids, 1 heading leaks*

**Christian** (12)
- `ambrose-select-works` — Select Works and Letters — *2,093 dup ids, 11 heading leaks, 128 short*
- `eusebius-church-history` — Church History and Life of Constantine — *1,881 dup ids, 195 heading leaks, 292 short*
- `augustine-confessions-enchiridion-ccel` — Confessions and Enchiridion (CCEL) — *1,092 dup ids, 49 heading leaks, 688 short*
- `anf01-early-fathers` — Apostolic Fathers, Justin Martyr, Irenaeus — *730 dup ids, 395 heading leaks*
- `jerome-letters-works` — Letters and Select Works — *1,002 dup ids, 20 heading leaks, 249 short*
- `athanasius-select-works` — Select Works and Letters — *909 dup ids, 63 heading leaks, 877 short*
- `cyril-nazianzus-select-works` — Select Works of Cyril of Jerusalem and Gregory of Nazianzus — *820 dup ids, 39 heading leaks, 307 short*
- `chrysostom-homilies-matthew` — Homilies on the Gospel of Matthew — *465 dup ids, 2 heading leaks, 320 short*
- `basil-letters-works` — Letters and Select Works — *364 dup ids, 4 heading leaks, 304 short*
- `gregory-nyssa-select-works` — Dogmatic Treatises and Select Works — *240 dup ids, 13 heading leaks, 133 short*
- `luther-good-works` — Treatise on Good Works — *134 dup ids*
- `calvin-treatise-relics` — A Treatise on Relics — *15 dup ids, 2 heading leaks*

**Hindu** (1)
- `upanishads` — The Upanishads — *196 dup ids*

**Greek Philosophy** (1)
- `diogenes-lives` — The Lives and Opinions of Eminent Philosophers — *16 dup ids, 2 heading leaks*

**Buddhist** (1)
- `buddha-life-herold` — The Life of Buddha — *775 dup ids, 2 heading leaks*

**Jewish** (3)
- `josephus-antiquities` — Antiquities of the Jews — *249 dup ids, 2 heading leaks*
- `pirke-avot` — Pirke Avot (The Sayings of the Jewish Fathers) — *123 dup ids, 8 heading leaks*
- `josephus-wars-jews` — The Wars of the Jews — *20 dup ids, 2 heading leaks*

**Political Philosophy** (1)
- `marx-eighteenth-brumaire` — The Eighteenth Brumaire of Louis Bonaparte — *12 dup ids, 1 heading leaks*

**Islam** (1)
- `rumi-masnavi` — The Masnavi — *77 dup ids, 6 heading leaks*

### Heading leakage (parser) (19)

*Heading-shaped lines ("BOOK I", "CHAPTER 1") appearing as passage bodies. Fix: tighten heading detection at ingest. Passage content is intact.*

**Modern Philosophy** (1)
- `the-r-m-yan-of-v-lm-ki-ralph-griffith` — The Rámáyan of Válmíki — *498 heading leaks, 455 short*

**Christian** (1)
- `aquinas-summa-theologica` — Summa Theologica — *1,449 heading leaks*

**Greek Literature** (5)
- `gibbon-decline-fall` — The History of the Decline and Fall of the Roman Empire — *309 heading leaks*
- `shakespeare-the-tragedy-of-coriolanus` — The Tragedy of Coriolanus — *72 heading leaks*
- `shakespeare-alls-well-that-ends-well` — All’s Well That Ends Well — *61 heading leaks*
- `the-sundering-flood-william-morris-1897` — The Sundering Flood — *52 heading leaks*
- `shakespeare-the-tragedy-of-macbeth` — The Tragedy of Macbeth — *51 heading leaks*

**Hindu** (9)
- `ramayana-griffith` — The Ramayana — *498 heading leaks, 454 short*
- `the-yoga-vasishtha-maharamayana-of-valmiki-vol-3-valmiki` — The Yoga-Vasishtha Maharamayana of Valmiki - Vol 3 - pt 2 — *265 heading leaks, 231 short*
- `yoga-vasishtha-mitra-vol3-pt2` — The Yoga-Vāsiṣṭha Mahā-Rāmāyaṇa, Vol 3 pt 2 — *265 heading leaks, 231 short*
- `the-yoga-vasishtha-maharamayana-of-valmiki-vol-4-valmiki` — The Yoga-Vasishtha Maharamayana of Valmiki - Vol 4 - pt 2 — *226 heading leaks, 165 short*
- `yoga-vasishtha-mitra-vol4-pt2` — The Yoga-Vāsiṣṭha Mahā-Rāmāyaṇa, Vol 4 pt 2 — *226 heading leaks, 165 short*
- `yoga-vasishtha-mitra-vol4-pt1` — The Yoga-Vāsiṣṭha Mahā-Rāmāyaṇa, Vol 4 pt 1 — *215 heading leaks, 189 short*
- `the-yoga-vasishtha-maharamayana-of-valmiki-vol-2-valmiki` — The Yoga-Vasishtha Maharamayana of Valmiki - Vol 2 - pt 2 — *127 heading leaks, 119 short*
- `yoga-vasishtha-mitra-vol2-pt2` — The Yoga-Vāsiṣṭha Mahā-Rāmāyaṇa, Vol 2 pt 2 — *127 heading leaks, 119 short*
- `yoga-vasishtha-mitra-vol2-pt1` — The Yoga-Vāsiṣṭha Mahā-Rāmāyaṇa, Vol 2 pt 1 — *83 heading leaks*

**Celtic** (1)
- `gods-fighting-men-gregory` — Gods and Fighting Men — *88 heading leaks*

**Roman Philosophy** (1)
- `morals-of-a-happy-life-benefits-anger-and-seneca` — Morals of a Happy Life & Benefits & Anger and Clemency — *57 heading leaks*

**Norse** (1)
- `prose-edda` — The Prose Edda (Younger Edda) — *63 heading leaks*

### Heading leakage (minor) (119)

*A small number of heading-shaped lines leaked into passage bodies. Cosmetic; reader can navigate around them.*

**Modern Philosophy** (30)
- `kant-critique-pure-reason` — Critique of Pure Reason — *50 heading leaks*
- `mill-system-logic-vol2` — A System of Logic, Vol 2 — *49 heading leaks*
- `democracy-in-america-vol-2-tocquevilla` — Democracy in America - Vol 2 — *44 heading leaks*
- `essay-concerning-humane-understanding-vol-2-john-locke` — Essay Concerning Humane Understanding - Vol 2 — *38 heading leaks*
- `democracy-in-america-vol-1-tocquevilla` — Democracy in America - Vol 1 — *37 heading leaks*
- `schopenhauer-world-will-vol3` — The World as Will and Idea, Vol 3 — *35 heading leaks*
- `mill-system-logic-vol1` — A System of Logic, Vol 1 — *34 heading leaks*
- `essay-concerning-humane-understanding-vol-1` — Essay Concerning Humane Understanding - Vol 1 — *30 heading leaks*
- `a-wanderer-in-the-sprit-lands-franchezzo-1896` — A Wanderer in the Sprit Lands — *27 heading leaks*
- `hegel-logic` — The Logic of Hegel — *25 heading leaks*
- `leopardi-essays-dialogues` — Essays and Dialogues — *23 heading leaks*
- `locke-essay-vol2` — An Essay Concerning Human Understanding, Vol. 2 — *21 heading leaks*
- `russell-geometry-foundations` — An Essay on the Foundations of Geometry — *21 heading leaks*
- `the-canterbury-tales-other-works-of-chaucer-geoffery-chaucer` — The Canterbury Tales & Other Works of Chaucer — *14 heading leaks*
- `the-martyrs-of-science-the-lives-of-galileo` — The Martyrs of Science - The lives of Galileo & Tycho Brahe & Kepler — *14 heading leaks*
- `hume-enquiry-understanding` — An Enquiry Concerning Human Understanding — *13 heading leaks*
- `moore-principia-ethica` — Principia Ethica — *13 heading leaks*
- `schopenhauer-world-will-vol2` — The World as Will and Idea, Vol 2 — *13 heading leaks*
- `goethe-wilhelm-meister-vol2` — Wilhelm Meister's Apprenticeship and Travels, Vol 2 — *11 heading leaks*
- `religious-development-thought-in-ancient-egypt-james-breaste` — Religious Development & Thought in Ancient Egypt — *11 heading leaks*
- `the-varieties-of-religous-experience-william-james-1902` — The Varieties of Religous Experience — *11 heading leaks*
- `kant-critique-practical-reason` — Critique of Practical Reason — *9 heading leaks*
- `the-birth-of-the-war-god-a-poem-ralph-griffith` — The Birth of the War-God - A Poem by Kálidása — *9 heading leaks*
- `hume-enquiry-morals` — An Enquiry Concerning the Principles of Morals — *8 heading leaks*
- `the-udana-gm-strong-1902-no` — The Udana — *8 heading leaks*
- `archimedes-thomas-heath` — Archimedes — *7 heading leaks*
- `joyful-wisdom` — The Joyful Wisdom (La Gaya Scienza) — *7 heading leaks*
- `kant-prolegomena` — Prolegomena to Any Future Metaphysics — *7 heading leaks*
- `schopenhauer-world-will-vol1` — The World as Will and Idea, Vol 1 — *6 heading leaks*
- `the-gospel-of-ramakrishna-swami-abhedananda-19` — The Gospel of Ramakrishna — *6 heading leaks*

**Christian** (7)
- `interior-castle-teresa` — The Interior Castle — *28 heading leaks*
- `unknown-life-jesus-notovitch` — The Unknown Life of Jesus Christ — *26 heading leaks*
- `aquarian-gospel` — The Aquarian Gospel of Jesus Christ — *21 heading leaks*
- `luther-genesis-vol1` — Commentary on Genesis, Vol 1 — *15 heading leaks*
- `intermediate-types-carpenter` — Intermediate Types among Primitive Folk — *12 heading leaks*
- `trial-christ-cheeseman` — The Trial of Christ — *9 heading leaks*
- `ayer-ancient-church-history` — A Source Book for Ancient Church History — *8 heading leaks*

**Greek Literature** (19)
- `tacitus-oratory` — A Dialogue Concerning Oratory — *50 heading leaks*
- `folklore-shakespeare-dyer` — Folk-lore of Shakespeare — *47 heading leaks*
- `odyssey-pope` — The Odyssey (Pope) — *46 heading leaks*
- `shakespeare-the-two-noble-kinsmen` — The Two Noble Kinsmen — *45 heading leaks*
- `shakespeare-the-tragedy-of-julius-caesar` — The Tragedy of Julius Caesar — *44 heading leaks*
- `iliad` — Iliad — *18 dup ids, 25 heading leaks*
- `shakespeare-the-tragedy-of-antony-and-cleopatra` — The Tragedy of Antony and Cleopatra — *41 heading leaks*
- `shakespeare-king-richard-the-third` — King Richard the Third — *35 heading leaks*
- `shakespeare-pericles-prince-of-tyre` — Pericles, Prince of Tyre — *34 heading leaks*
- `shakespeare-king-henry-the-eighth` — King Henry the Eighth — *31 heading leaks*
- `shakespeare-the-tragedy-of-hamlet-prince-of` — The Tragedy of Hamlet, Prince of Denmark — *23 heading leaks*
- `shakespeare-cymbeline` — Cymbeline — *19 heading leaks*
- `shakespeare-the-two-gentlemen-of-verona` — The Two Gentlemen of Verona — *14 heading leaks*
- `shakespeare-the-winters-tale` — The Winter’s Tale — *14 heading leaks*
- `shakespeare-measure-for-measure` — Measure for Measure — *12 heading leaks*
- `aristophanes-peace` — Peace — *7 heading leaks*
- `shakespeare-as-you-like-it` — As You Like It — *6 heading leaks*
- `shakespeare-the-first-part-of-henry-the` — The First Part of Henry the Sixth — *6 heading leaks*
- `shakespeare-the-taming-of-the-shrew` — The Taming of the Shrew — *6 heading leaks*

**Hindu** (8)
- `kama-sutra-burton` — The Kama Sutra of Vatsyayana — *44 heading leaks*
- `yoga-vasishtha-mitra-vol3-pt1` — The Yoga-Vāsiṣṭha Mahā-Rāmāyaṇa, Vol 3 pt 1 — *44 heading leaks*
- `science-breath-yogi-ramacharaka` — The Science of Breath — *32 heading leaks*
- `garuda-purana` — The Garuda Purana — *17 heading leaks*
- `history-sanskrit-literature-macdonell` — A History of Sanskrit Literature — *13 heading leaks*
- `vedanta-sutras-sankara` — The Vedanta-Sutras with the Commentary by Sankaracarya — *12 heading leaks*
- `kalidasa-birth-war-god` — The Birth of the War-God (Kumārasaṃbhava) — *9 heading leaks*
- `arnold-hindu-literature` — Hindu Literature — *7 heading leaks*

**Greek Philosophy** (6)
- `copernican-acceptance-stimson` — The Gradual Acceptance of the Copernican Theory of the Universe — *19 heading leaks*
- `darwin-expression-emotions` — The Expression of the Emotions in Man and Animals — *19 heading leaks*
- `plato-timaeus` — Timaeus — *9 heading leaks*
- `archimedes-heath` — The Works of Archimedes — *7 heading leaks*
- `hippocrates-aphorisms` — Aphorisms — *6 heading leaks*
- `proclus-euclid` — Commentaries on the First Book of Euclid — *6 heading leaks*

**Hermetic** (9)
- `atlantis-donnelly` — Atlantis: The Antediluvian World — *44 heading leaks*
- `sun-lore-olcott` — Sun Lore of All Ages — *13 heading leaks*
- `devil-worship-france-waite` — Devil Worship in France — *11 heading leaks*
- `illustrations-masonry-morgan` — Illustrations of Masonry — *10 heading leaks*
- `huna-theory-long` — Self-Suggestion and the New Huna Theory of Mesmerism — *8 heading leaks*
- `great-pyramid-smyth` — The Great Pyramid (A Miracle in Stone) — *7 heading leaks*
- `migration-symbols-d-alviella` — The Migration of Symbols — *7 heading leaks*
- `steiner-higher-worlds` — Knowledge of the Higher Worlds and Its Attainment — *7 heading leaks*
- `meaning-masonry-wilmshurst` — The Meaning of Masonry — *6 heading leaks*

**Buddhist** (2)
- `gaudama-burmese-vol1` — The Life or Legend of Gaudama, the Buddha of the Burmese, Vol 1 — *32 heading leaks*
- `gaudama-burmese-vol2` — The Life or Legend of Gaudama, the Buddha of the Burmese, Vol 2 — *10 heading leaks*

**Jewish** (6)
- `song-of-songs-translation` — The Song of Songs — *28 heading leaks*
- `ancient-jewish-proverbs` — Ancient Jewish Proverbs — *24 heading leaks*
- `jerusalem-herod-saladin-besant` — Jerusalem: the City of Herod and Saladin — *19 heading leaks*
- `prolegomena-to-the-history-of-israel-julius-wellhausen` — Prolegomena to the History of Israel — *11 heading leaks*
- `jesus-essene-hartmann` — Jesus an Essene — *9 heading leaks*
- `maimonides-guide` — The Guide for the Perplexed — *9 heading leaks*

**Political Philosophy** (11)
- `mill-political-economy` — Principles of Political Economy — *41 heading leaks*
- `tocqueville-old-regime` — The State of Society in France Before the Revolution of 1789 — *34 heading leaks*
- `tocqueville-democracy-vol2` — Democracy in America, Vol 2 — *27 heading leaks*
- `smith-moral-sentiments` — The Theory of Moral Sentiments — *26 heading leaks*
- `tocqueville-democracy-vol1` — Democracy in America, Vol 1 — *25 heading leaks*
- `vindication-rights-woman` — A Vindication of the Rights of Woman — *25 heading leaks*
- `ideal-commonwealths` — Ideal Commonwealths — *10 heading leaks*
- `the-origin-of-the-family-private-property-the-engels` — The origin of the family & private property & the state — *9 heading leaks*
- `wealth-of-nations` — The Wealth of Nations — *9 heading leaks*
- `discourses-on-the-first-decade-of-titus-livius-machiavelli` — Discourses on the First Decade of Titus Livius — *8 heading leaks*
- `marx-critique-political-economy` — A Contribution to the Critique of Political Economy — *7 heading leaks*

**Celtic** (2)
- `baring-gould-were-wolves` — The Book of Were-Wolves — *18 heading leaks*
- `cornwall-traditions-vol1-bottrell` — Traditions and Hearthside Stories of West Cornwall, Vol 1 — *8 heading leaks*

**Mesoamerican** (2)
- `back-black-mans-mind-dennett` — At the Back of the Black Man's Mind — *10 heading leaks*
- `dawn-world-merriam` — The Dawn of the World — *6 heading leaks*

**Islam** (1)
- `some-religious-and-moral-teachings-al-ghazzali` — Some religious and moral teachings — *12 heading leaks*

**Egyptian** (1)
- `egypt-religious-development-petrie` — Religious Development and Thought in Ancient Egypt — *11 heading leaks*

**Mesopotamian** (2)
- `the-seven-great-monarchies-of-the-ancient-eastern-george-raw` — The Seven Great Monarchies Of The Ancient Eastern World - Vol 7 - The Sassanian (New Persian) Empire — *29 heading leaks*
- `evolution-dragon-smith` — The Evolution of the Dragon — *10 heading leaks*

**Roman Philosophy** (2)
- `seneca-benefits` — On Benefits — *7 heading leaks*
- `the-republic-cicero` — The republic — *7 heading leaks*

**Confucian** (2)
- `the-shih-king-book-of-poetry-james-legge` — The Shih King (Book of Poetry) — *16 heading leaks*
- `chinese-literature-legge` — Chinese Literature (Legge) — *13 heading leaks*

**Greek** (2)
- `hesiod-shield-hercules-elton` — The Remains of Hesiod the Ascræan & The Shield of Hercules — *9 heading leaks*
- `astrology-greeks-romans-cumont` — Astrology and Religion Among the Greeks and Romans — *6 heading leaks*

**Norse** (2)
- `volsunga-saga` — The Volsunga Saga — *27 heading leaks*
- `norse-discovery-america-anderson` — The Norse Discovery of America — *17 heading leaks*

**Theosophy** (1)
- `isis-unveiled-vol1-blavatsky` — Isis Unveiled, Volume 1 (Science) — *32 heading leaks*

**(none)** (1)
- `gospel-ramakrishna-nikhilananda` — gospel-ramakrishna-nikhilananda — *6 heading leaks*

**Comparative Religion** (2)
- `sacred-books-east-wilson` — Sacred Books of the East (Wilson Anthology) — *42 heading leaks*
- `monier-williams-buddhism` — Buddhism in Its Connexion with Brahmanism and Hinduism — *30 heading leaks*

**Rastafari** (1)
- `holy-piby` — The Holy Piby — *28 heading leaks*

### Many short passages (154)

*Large fraction of passages are very short. Often legitimate (dialogue, speaker labels in plays); sometimes ingest fragments worth reviewing.*

**Modern Philosophy** (26)
- `the-writings-of-origen-vol-2-origen` — The writings of Origen - Vol 2 — *563 heading leaks, 2,946 short*
- `thus-spake-zarathustra` — Thus Spake Zarathustra — *71 dup ids, 67 heading leaks, 162 short*
- `the-writings-of-origen-vol-1-origen` — The writings of Origen - Vol 1 — *110 heading leaks, 2,034 short*
- `montaigne-essays` — Essays of Michel de Montaigne — *106 heading leaks, 171 short*
- `goethe-wilhelm-meister-vol1` — Wilhelm Meister's Apprenticeship and Travels, Vol 1 — *95 heading leaks, 108 short*
- `jaina-sutras-part-2-hermann-jacobi-1884` — Jaina Sutras - Part 2 — *58 heading leaks, 241 short*
- `the-kama-sutra-vatsyayana` — The Kama Sutra — *55 heading leaks, 150 short*
- `history-of-utah-1540-1886-hubert-bancroft-1889` — History of Utah 1540-1886 — *54 heading leaks, 348 short*
- `yajur-veda-white-ralph-griffith-1899` — Yajur Veda (white) — *39 heading leaks, 866 short*
- `plotinos-complete-works-vol-4-plotinos` — Plotinos - Complete Works - Vol 4 — *22 heading leaks, 359 short*
- `goethe-theory-colours` — Theory of Colours — *21 heading leaks, 1,076 short*
- `goethe-poems` — The Poems of Goethe — *19 heading leaks, 312 short*
- `poems-goethe-tr-edgar-bowr` — Poems — *19 heading leaks, 312 short*
- `shibboleth-a-templar-monitor-george-connor-1894` — Shibboleth A Templar Monitor — *17 heading leaks, 545 short*
- `essays-adam-smith` — Essays on Philosophical Subjects — *14 heading leaks, 113 short*
- `bruno-heroic-enthusiasts` — The Heroic Enthusiasts — *13 heading leaks, 174 short*
- `numbers-their-occult-power-mystic-virtues-w-wynn-westcott-19` — Numbers - Their Occult Power & Mystic Virtues — *13 heading leaks, 523 short*
- `thrice-greatest-hermes-vol-3-grs-mead-1906` — Thrice-Greatest Hermes - Vol 3 — *13 heading leaks, 624 short*
- `iamblichus-on-the-mysteries-of-the-egyptians-chaldeans-porph` — Iamblichus on the mysteries of the Egyptians & Chaldeans & Assyrians — *11 heading leaks, 330 short*
- `plotinos-complete-works-vol-1-plotinos` — Plotinos - Complete Works - Vol 1 — *11 heading leaks, 183 short*
- `the-mesnavi-the-acts-of-the-adepts-james-redhouse-1881` — The Mesnavi & The Acts of the Adepts — *11 heading leaks, 295 short*
- `abominable-snowmen-ivan-sanderson-1961` — Abominable Snowmen — *10 heading leaks, 256 short*
- `rumanian-bird-and-beast-stories-moses-gaster` — Rumanian Bird and Beast Stories — *9 heading leaks, 318 short*
- `plotinos-complete-works-vol-2-plotinos` — Plotinos - Complete Works - Vol 2 — *8 heading leaks, 159 short*
- `berkeley-works-vol1` — The Works of George Berkeley, Vol 1 — *7 heading leaks, 233 short*
- `nicholson-literary-arabs` — A Literary History of the Arabs — *7 heading leaks, 533 short*

**Christian** (13)
- `anf04-tertullian-cyprian` — Tertullian II, Minucius Felix, and Cyprian — *306 dup ids, 70 heading leaks, 503 short*
- `pagan-christs-robertson` — Pagan Christs — *185 heading leaks, 248 short*
- `tertullian-volume-1` — Writings, Volume I: Apology + Doctrinal & Controversial Works — *95 dup ids, 83 heading leaks, 1,347 short*
- `augustine-city-of-god-ccel` — City of God and On Christian Doctrine (CCEL) — *12 dup ids, 115 heading leaks, 160 short*
- `origen-writings` — The Writings of Origen — *110 heading leaks, 272 short*
- `newman-essays` — Newman: Collected Essays — *29 heading leaks, 413 short*
- `milton-poems` — The Poems of Milton — *28 heading leaks, 135 short*
- `woman-position-influence-donaldson` — Woman: Her Position and Influence in Ancient Greece and Rome — *28 heading leaks, 148 short*
- `augustine-donatist-controversy` — Writings in Connection with the Donatist Controversy — *26 heading leaks, 1,219 short*
- `chrysostom-homilies-galatians-ephesians` — Homilies on Galatians, Ephesians, and more — *5 dup ids, 20 heading leaks, 278 short*
- `man-of-sorrows-petrie` — The Man of Sorrows — *24 heading leaks, 207 short*
- `hymns-eastern-church-neale` — Hymns of the Eastern Church — *12 heading leaks, 236 short*
- `chrysostom-homilies-timothy-hebrews` — Homilies on Timothy, Titus, Philemon, and Hebrews — *7 heading leaks, 676 short*

**Greek Literature** (8)
- `shakespeare-complete` — The Complete Works of William Shakespeare — *630 heading leaks, 2,738 short*
- `shakespeare-the-tempest` — The Tempest — *70 heading leaks, 114 short*
- `invasion-india-alexander` — The Invasion of India by Alexander the Great — *25 heading leaks, 318 short*
- `shakespeare-the-tragedy-of-romeo-and-juliet` — The Tragedy of Romeo and Juliet — *13 heading leaks, 109 short*
- `shakespeare-the-tragedy-of-othello-the-moor` — The Tragedy of Othello, the Moor of Venice — *12 heading leaks, 104 short*
- `bacon-wisdom-ancients` — Bacon's Essays & Wisdom of the Ancients — *8 heading leaks, 120 short*
- `shakespeare-the-first-part-of-king-henry` — The First Part of King Henry the Fourth — *7 heading leaks, 124 short*
- `shakespeare-a-midsummer-nights-dream` — A Midsummer Night’s Dream — *6 heading leaks, 115 short*

**Hindu** (13)
- `rig-veda-griffith` — The Hymns of the Rigveda — *793 heading leaks, 1,173 short*
- `the-yoga-vasishtha-maharamayana-of-valmiki-vol-1-valmiki` — The Yoga-Vasishtha Maharamayana of Valmiki - Vol 1 — *273 heading leaks, 310 short*
- `yoga-vasishtha-mitra-vol1` — The Yoga-Vāsiṣṭha Mahā-Rāmāyaṇa, Vol 1 — *273 heading leaks, 310 short*
- `vishnupuranam-dutt` — Vishnupuranam (Dutt) — *142 heading leaks, 232 short*
- `the-upanishads-max-muller-1879` — The_Upanishads — *114 heading leaks, 522 short*
- `upanishads-muller-part1` — The Upanishads (Müller, Part 1) — *80 heading leaks, 237 short*
- `upanishads-muller-part2` — The Upanishads (Müller, Part 2) — *54 heading leaks, 172 short*
- `kalidasa-sakoontala` — Sakoontala, or The Lost Ring — *41 heading leaks, 824 short*
- `sakoontala-the-lost-ring-an-indian-drama-kalidasa-tr-monier-` — Sakoontala (The Lost Ring) - An Indian Drama — *41 heading leaks, 824 short*
- `yajur-veda-white-griffith` — The White Yajur Veda (Vajasaneyi Saṃhitā) — *39 heading leaks, 866 short*
- `dakshinamurti-stotra` — Dakshinamurti Stotra — *15 heading leaks, 132 short*
- `vedanta-sutras-ramanuja` — The Vedanta-Sutras with the Commentary by Ramanuja — *15 heading leaks, 152 short*
- `vedic-hymns-part1` — Vedic Hymns, Part 1 — *8 heading leaks, 2,889 short*

**Greek Philosophy** (14)
- `proclus-theology-plato` — On the Theology of Plato — *371 heading leaks, 383 short*
- `plato-republic` — Republic — *318 dup ids, 1 heading leaks, 884 short*
- `galileo-roman-curia-von-gebler` — Galileo Galilei and the Roman Curia — *59 heading leaks, 166 short*
- `culpeper-complete-herbal` — The Complete Herbal — *49 heading leaks, 388 short*
- `galen-natural-faculties` — On the Natural Faculties — *45 heading leaks, 240 short*
- `sextus-empiricus` — Sextus Empiricus and Greek Scepticism — *45 heading leaks, 197 short*
- `grote-plato-companions-vol2` — Plato and the Other Companions of Sokrates, Vol 2 — *33 heading leaks, 351 short*
- `grote-plato-companions-vol1` — Plato and the Other Companions of Sokrates, Vol 1 — *24 heading leaks, 245 short*
- `plotinus-complete-vol4` — Plotinus: Complete Works, Vol 4 — *22 heading leaks, 359 short*
- `darwin-descent-man-full` — The Descent of Man and Selection in Relation to Sex — *19 heading leaks, 189 short*
- `grote-plato-companions-vol3` — Plato and the Other Companions of Sokrates, Vol 3 — *19 heading leaks, 277 short*
- `grote-plato-companions-vol4` — Plato and the Other Companions of Sokrates, Vol 4 — *11 heading leaks, 321 short*
- `iamblichus-mysteries` — On the Mysteries of the Egyptians, Chaldeans, and Assyrians — *11 heading leaks, 330 short*
- `plotinus-complete-vol1` — Plotinus: Complete Works, Vol 1 — *11 heading leaks, 183 short*

**Hermetic** (17)
- `natural-magic-agrippa` — The Philosophy of Natural Magic — *92 heading leaks, 373 short*
- `occult-science-india-jacolliot` — Occult Science in India — *86 heading leaks, 158 short*
- `secret-societies-keightley` — Secret Societies of the Middle Ages — *60 heading leaks, 107 short*
- `waite-rosicrucians` — The Real History of the Rosicrucians — *50 heading leaks, 153 short*
- `virgin-world-kingsford` — The Virgin of the World — *44 heading leaks, 313 short*
- `ahiman-rezon` — General Ahiman Rezon — *25 heading leaks, 313 short*
- `duncans-masonic-ritual` — Duncan's Masonic Ritual and Monitor — *24 heading leaks, 324 short*
- `initiation-bailey` — Initiation, Human and Solar — *23 heading leaks, 223 short*
- `internet-book-shadows` — Internet Book of Shadows — *23 heading leaks, 3,131 short*
- `shibboleth-templar-monitor` — Shibboleth: A Templar Monitor — *17 heading leaks, 545 short*
- `comte-st-germain-cooper-oakley` — The Comte de St. Germain — *15 heading leaks, 157 short*
- `pictorial-key-tarot-waite` — The Pictorial Key to the Tarot — *14 heading leaks, 113 short*
- `numbers-occult-westcott` — Numbers: Their Occult Power and Mystic Virtues — *13 heading leaks, 523 short*
- `thrice-greatest-hermes-vol3` — Thrice-Greatest Hermes, Vol 3 — *13 heading leaks, 624 short*
- `stolen-legacy-james` — Stolen Legacy — *11 heading leaks, 106 short*
- `witch-cult-murray` — The Witch-Cult in Western Europe — *7 heading leaks, 1,959 short*
- `proofs-conspiracy-robison` — Proofs of a Conspiracy — *6 heading leaks, 127 short*

**Buddhist** (4)
- `buddha-way-virtue-wagiswara` — The Buddha's Way of Virtue — *54 heading leaks, 108 short*
- `outlines-mahayana-suzuki` — Outlines of Mahayana Buddhism — *46 heading leaks, 239 short*
- `shinran-lloyd` — Shinran and His Work — *27 heading leaks, 201 short*
- `dhammapada-muller` — The Dhammapada & Sutta-Nipāta (Müller) — *26 heading leaks, 441 short*

**Jewish** (10)
- `babylonian-talmud-rodkinson` — The Babylonian Talmud — *217 heading leaks, 4,934 short*
- `mishna-18-rabbinowicz` — Eighteen Treatises from the Mishna — *162 heading leaks, 180 short*
- `book-of-enoch` — The Book of Enoch — *112 heading leaks, 239 short*
- `jerahmeel-gaster` — The Chronicles of Jerahmeel — *50 heading leaks, 114 short*
- `goldziher-hebrew-mythology` — Mythology among the Hebrews — *36 heading leaks, 188 short*
- `talmud-polano` — The Talmud: Selections — *17 heading leaks, 122 short*
- `wellhausen-prolegomena` — Prolegomena to the History of Ancient Israel — *14 heading leaks, 1,365 short*
- `ot-historical-records-king` — The Old Testament in the Light of the Historical Records of Assyria and Babylonia — *13 heading leaks, 211 short*
- `sayce-egypt-hebrews` — The Egypt of the Hebrews and Herodotos — *12 heading leaks, 247 short*
- `standard-prayer-book-singer` — The Standard Prayer Book — *7 heading leaks, 217 short*

**Mesoamerican** (3)
- `old-north-trail-mcclintock` — The Old North Trail — *40 heading leaks, 117 short*
- `tewa-songs-spinden` — Songs of the Tewa — *9 heading leaks, 134 short*
- `myths-mexico-peru-spence` — Myths of Mexico and Peru — *7 heading leaks, 121 short*

**Islam** (9)
- `manual-of-hadith` — A Manual of Hadith — *542 dup ids, 2 heading leaks, 1,187 short*
- `quran` — Quran — *111 heading leaks, 135 short*
- `the-kashf-al-mahj-b-oldest-persian-treatise-ali-ibn-usman-hu` — The Kashf al-mahjúb (Oldest Persian treatise on Súfiism) — *76 heading leaks, 131 short*
- `nahjul-balagha` — Nahjul Balagha (Peak of Eloquence) — *75 heading leaks, 1,771 short*
- `oriental-mysticism-palmer` — Oriental Mysticism — *32 heading leaks, 115 short*
- `mesnavi-acts-adepts-redhouse` — The Mesnavi and the Acts of the Adepts — *11 heading leaks, 295 short*
- `the-mesnevi-rumi` — The Mesnevi — *11 heading leaks, 268 short*
- `arabian-poetry-clouston` — Arabian Poetry — *10 heading leaks, 346 short*
- `history-literary-of-the-arabs-reynold-nicholson` — History (Literary) of the Arabs — *7 heading leaks, 571 short*

**Egyptian** (3)
- `book-of-dead-renouf` — The Egyptian Book of the Dead — *430 heading leaks, 644 short*
- `egyptian-myth-legend` — Egyptian Myth and Legend — *31 heading leaks, 522 short*
- `sayce-religions-egypt-babylonia` — The Religions of Ancient Egypt and Babylonia — *22 heading leaks, 135 short*

**Mesopotamian** (1)
- `chaldean-genesis-smith` — The Chaldean Account of Genesis — *42 heading leaks, 405 short*

**Roman Philosophy** (3)
- `pliny-natural-history-vol4` — The Natural History of Pliny, Vol 4 — *15 heading leaks, 270 short*
- `seneca-physical-science-nero` — Physical Science in the Time of Nero — *8 heading leaks, 107 short*
- `pliny-natural-history-vol6` — The Natural History of Pliny, Vol 6 — *7 heading leaks, 1,001 short*

**Confucian** (1)
- `history-chinese-literature-giles` — A History of Chinese Literature — *7 heading leaks, 188 short*

**Taoist** (2)
- `carus-laotzu-study` — Lao-tze: A Study in Chinese Philosophy — *12 heading leaks, 106 short*
- `lao-tzu-a-study-in-chinese-philosophy-thomas-watters` — Lao-tzu - A Study in Chinese Philosophy — *12 heading leaks, 106 short*

**Gnostic** (2)
- `gnostics-remains-king` — The Gnostics and Their Remains — *16 heading leaks, 267 short*
- `fragments-faith-mead` — Fragments of a Faith Forgotten — *11 heading leaks, 777 short*

**Theosophy** (5)
- `secret-doctrine-vol3-blavatsky` — The Secret Doctrine, Vol. 3 of 4 — *44 heading leaks, 128 short*
- `secret-doctrine-vol1-blavatsky` — The Secret Doctrine, Vol. 1 of 4 — *35 heading leaks, 154 short*
- `isis-unveiled-vol2-blavatsky` — Isis Unveiled, Volume 2 (Theology) — *26 heading leaks, 113 short*
- `secret-doctrine-vol2-blavatsky` — The Secret Doctrine, Vol. 2 of 4 — *16 heading leaks, 174 short*
- `secret-doctrine-vol4-blavatsky` — The Secret Doctrine, Vol. 4 of 4 — *10 heading leaks, 118 short*

**Shinto** (1)
- `no-plays-japan-waley` — The Nō Plays of Japan — *17 heading leaks, 1,062 short*

**Persian Literature** (1)
- `arabian-nights-burton` — The Book of the Thousand Nights and a Night — *6 dup ids, 9 heading leaks, 247 short*

**Stoic** (1)
- `arnold-roman-stoicism` — Roman Stoicism — *19 heading leaks, 570 short*

**(none)** (3)
- `dead-sea-scrolls-vermes` — dead-sea-scrolls-vermes — *38 heading leaks, 905 short*
- `dead-sea-scrolls-garcia-martinez` — dead-sea-scrolls-garcia-martinez — *32 heading leaks, 389 short*
- `think-grow-rich-hill` — think-grow-rich-hill — *17 heading leaks, 287 short*

**Sikh** (4)
- `sikh-religion-vol1-macauliffe` — The Sikh Religion, Volume 1 — *73 heading leaks, 352 short*
- `sikh-religion-vol5-macauliffe` — The Sikh Religion, Volume 5 — *34 heading leaks, 506 short*
- `sikh-religion-vol2-macauliffe` — The Sikh Religion, Volume 2 — *27 heading leaks, 323 short*
- `sikh-religion-vol3-macauliffe` — The Sikh Religion, Volume 3 — *12 heading leaks, 405 short*

**Slavic** (1)
- `songs-russian-people-ralston` — The Songs of the Russian People — *23 heading leaks, 501 short*

**Comparative Religion** (1)
- `folklore-holy-land` — Folk-lore of the Holy Land — *13 heading leaks, 501 short*

**Zoroastrian** (3)
- `zend-avesta-part1` — The Zend-Avesta, Part 1: Vendidad — *71 heading leaks, 806 short*
- `zend-avesta-part3` — The Zend-Avesta, Part 3: Yasna, Visparad, Afrinagan, and Gahs — *41 heading leaks, 896 short*
- `zend-avesta-part2` — The Zend-Avesta, Part 2: Sirozahs, Yasts, and Nyayis — *23 heading leaks, 878 short*

**Tibetan Buddhist** (1)
- `milarepa-evans-wentz` — Tibet's Great Yogi Milarepa — *27 heading leaks, 198 short*

**Jain** (2)
- `uttaradhyayana-sutra` — Uttaradhyayana Sutra — *276 heading leaks, 1,297 short*
- `jaina-sutras-part2` — Jaina Sutras, Part 2 — *38 heading leaks, 368 short*

**Witchcraft / Folk Religion** (1)
- `aradia-gospel-witches-leland` — Aradia, or the Gospel of the Witches — *49 heading leaks, 226 short*

**Mandaean** (1)
- `ginza-rabba` — Ginza Rabba (The Great Treasure) — *40 heading leaks, 833 short*

---

## 7. High-priority repair list

The top ten texts from `corpus_audit.py`'s structural-duplicate priority queue. *Severity* is the count of excess passage-id collisions (i.e. how many extra passages share an id with another passage in the same text). Fixing these would clear the largest share of the corpus's structural mess in the smallest number of operations.

| Rank | Text | Title | Issue family | Severity |
|---:|---|---|---|---:|
| 1 | `quran` | Quran | missing_book_level | 158,458 |
| 2 | `jataka` | The Jātaka | missing_book_level | 8,895 |
| 3 | `ambrose-select-works` | Select Works and Letters | unknown | 2,093 |
| 4 | `eusebius-church-history` | Church History and Life of Constantine | front_matter_absorbed | 1,881 |
| 5 | `expositor-bible` | The Expositor's Bible | regex_partial_detection | 1,720 |
| 6 | `augustine-confessions-enchiridion-ccel` | Confessions and Enchiridion (CCEL) | front_matter_absorbed | 1,092 |
| 7 | `calvin-letters` | Letters of John Calvin | missing_book_level | 1,022 |
| 8 | `jerome-letters-works` | Letters and Select Works | unknown | 1,002 |
| 9 | `athanasius-select-works` | Select Works and Letters | missing_book_level | 909 |
| 10 | `cyril-nazianzus-select-works` | Select Works of Cyril of Jerusalem and Gregory of Nazianzus | missing_book_level | 820 |

**Recurring patterns:**

- **`quran`** — single largest dup-ID collision. Many translations share id `1.1` for sura 1, verse 1, etc. Likely a missing book/sura level. *Re-ingest with sura-as-l1 parser.*
- **`jataka`** — multi-volume Buddhist tales with chapter-only hierarchy across volumes. *Add volume-as-l1 to parser.*
- **CCEL Christian patristic cluster** (`ambrose-select-works`, `anf01-early-fathers`, `eusebius-church-history`, `augustine-confessions-enchiridion-ccel`, `athanasius-select-works`, `chrysostom-homilies-matthew`, `jerome-letters-works`, `cyril-nazianzus-select-works`, `basil-letters-works`) — patristic series with letters/homilies/treatises bundled per volume. The parser keys by chapter only; letters from different volumes collide. *Volume-aware parser pass should clear most of these together.*
- **`expositor-bible`** — series id shared across four bible-book volumes; chapter ids collide. See `DUPLICATE_IDS.md`.

**None of these affect the *raw* text.** They are navigation and locator problems on top of intact content.

---

## 8. Reading Room status

The Reading Room (`workspace-hub/archive/`) is a separate surface from the canonical library. It contains 205 hand-edited Markdown chapters or fragments, all reachable through the deeper shelves. Its cleanliness is editorial, not parser-driven.

- **Entries on disk:** 205
- **All reachable** through `index.md` + `shelves.md`
- **Conform to Source Integrity Standard v1** ("`## Primary Text`" structure): 10
- **Older format** (readable but pre-SIS): 195

"Older format" entries are not broken. They predate the v1 discipline that visually separates source verses from Atlas commentary. Migration is unhurried.

Reading Room cleanliness is **independent** of canonical-corpus cleanliness. A Reading Room entry can be SIS-conforming and still soft-link to a canonical text that has parser issues, and vice versa.

---

## 9. Definitions

These are the terms used above. They come from `05_scripts/final_validation.py` and `05_scripts/corpus_audit.py`; the boundary lines are recorded here so future readers do not have to re-derive them.

- **Clean** — `final_validation.py` reports `status: clean`. Zero passage-id duplicates, low heading-leak count, balanced segment sizes. The reader's structural view matches the source's structure.
- **Acceptable** — `status: acceptable`. Minor issues only — small leakage, uneven segments, or many very-short passages. Usable today.
- **Needs work** — `status: needs_work`. At least one parser or structural issue substantial enough that the reader's view is uneven. **Does not mean the text is corrupted or lost.**
- **Integrity issue** — a passage that does not appear verbatim in the named raw source. Detected by `passage_subsequence_proof.py`. **Currently zero corpus-wide below 95 %**, including every "needs work" text.
- **Formatting issue** — visible irregularities in the reader's rendering (line breaks, encoding artifacts, stray OCR markers). Cosmetic; content unaffected.
- **Parser issue** — the ingest script produced incorrect structure (wrong hierarchy depth, wrong passage boundaries). Fix: re-ingest with a corrected parser. Content unaffected.
- **Metadata issue** — a `text.json` field is missing or non-standard (`source.url`, `source_quality`, `original_title`). Detected by `validate_metadata.py`. The 233 current schema warnings are nearly all in this category.
- **Duplicate-ID issue** — comes in two unrelated forms; see `DUPLICATE_IDS.md`. Type A (directory-level shared id, e.g. `bible` across 24 translation directories) is legitimate. Type B (passage-level collisions inside one text) is a parser problem and is what the "Duplicate-ID" issue family above refers to.

**A note on classification:** the *clean / acceptable / needs work* boundaries are inferred from `final_validation.py`'s thresholds, not encoded as flags on each `text.json`. The script applies the same rules every run; the labels in this report reflect the run on 2026-05-10.

---

## 10. What to fix first / what can wait / what is safe to read now

**Fix first** — only when in the mood for parser work:

- The single highest-leverage target is **`quran`** (~158k excess passage ids). One re-ingest restores navigability for the Quran's reader experience.
- After that, the **CCEL Christian patristic cluster**. Fixing the volume-aware parser pattern once would likely clear 8–10 needs-work texts together.
- **`jataka`** and the multi-volume Confucian/Buddhist series.

**Can wait** — present but low-impact:

- The 109 **acceptable** texts. They read end-to-end already.
- Schema metadata gaps. They make the validator chatty but do not affect what readers see.
- Reading Room SIS v1 migration. Older-format entries are readable; the standard is for new entries first.

**Safe to explore now** — no work required:

- All 666 **clean** texts. The reader's view matches the source.
- All 109 **acceptable** texts.
- The Reading Room's 5 front-shelf entries and any of the deeper-shelves entries. These are hand-edited.
- Any text on the Daily Reading whitelist (~198). The whitelist is itself a curated subset of the cleanest material.

