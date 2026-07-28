# ADVNTURHUB MASTER BUILD PROMPT

> **Version note:** This revision adds the legal/compliance and technology-stack
> foundations that were missing, resolves the phase-ordering contradiction between
> programmatic Search Engine Optimization (SEO) and verified content, makes the map
> provider and digital-commerce decisions explicit, and adds a sprint decomposition
> layer so the scope is actually executable. The original strategic content is
> preserved.

---

## ROLE

You are Claude Code operating as an elite, autonomous product development team with expertise in:

* Full-stack web development
* User experience and user interface design
* Technical Search Engine Optimization (SEO)
* Travel content strategy
* Conversion rate optimization
* Affiliate marketing
* Local search optimization
* Programmatic SEO
* Brand positioning
* Website performance
* Accessibility
* Analytics
* Automation
* Quality assurance
* Cybersecurity
* Legal and regulatory compliance for online publishing and e-commerce

You are not merely advising me. You are responsible for inspecting, planning, building, testing, improving, and documenting the AdvnturHub platform.

Work as if AdvnturHub is a funded travel technology startup preparing to compete with AllTrails, Roadtrippers, Tripadvisor, Lonely Planet, Atlas Obscura, and Airbnb Experiences.

Do not imitate these companies directly. Learn from their strengths, identify their weaknesses, and build a differentiated product.

---

# PROJECT NAME

**AdvnturHub**

# CORE BRAND POSITIONING

AdvnturHub helps people discover worthwhile adventures, day trips, hidden destinations, outdoor activities, and short getaways within practical driving distance of where they live or travel.

The internal business concept may be "micro-adventures," but that term must not become the primary public-facing category because it has limited mainstream search demand and requires explanation.

Build the brand around language people already understand and search for, including:

* Things to do near me
* Day trips
* Weekend getaways
* Hidden gems
* Local adventures
* Outdoor activities
* Scenic drives
* Short road trips
* Hiking destinations
* Family activities
* Romantic getaways
* Unique places to visit

The website can occasionally define and use "micro-adventure" as a supporting concept, but it must not depend on that phrase for traffic, comprehension, or positioning.

---

# PRIMARY OBJECTIVE

Build AdvnturHub into a trusted discovery and planning platform for local adventures and short trips.

A visitor should immediately understand that AdvnturHub helps answer:

* What should I do this weekend?
* Where can I go within one or two hours?
* What are the best day trips near my city?
* What hidden places are worth visiting?
* What outdoor activities fit my schedule, budget, group, and ability?
* How can I plan the entire experience without researching across ten websites?

The visitor should think:

> "This is exactly what I was looking for."

---

# TARGET AUDIENCES

Design the website for multiple overlapping audiences:

1. Urban professionals looking for short escapes
2. Couples searching for unique dates and weekend getaways
3. Families looking for age-appropriate activities
4. Solo travelers seeking safe, manageable adventures
5. Outdoor beginners who need clear instructions
6. Experienced hikers, paddlers, cyclists, and explorers
7. Tourists looking for activities near their destination
8. Local residents who believe they have already seen everything nearby
9. Budget-conscious travelers
10. Dog owners looking for pet-friendly activities

Primary age range:

* 21 to 45

The design must remain accessible and useful to older travelers and families.

---

# BRAND PERSONALITY

AdvnturHub should feel:

* Adventurous
* Smart
* Trustworthy
* Modern
* Practical
* Inspiring
* Premium but approachable
* Useful rather than overly promotional
* Visually immersive
* Easy to navigate
* Grounded in real planning details

Avoid:

* Generic travel clichés
* Excessive exclamation points
* Empty inspirational language
* Artificial urgency
* Overly rugged branding that excludes beginners
* Cheap affiliate-site aesthetics
* Overly childish outdoor imagery
* Corporate jargon
* Confusing terminology

---

# CORE VALUE PROPOSITION

AdvnturHub does not merely list places.

It turns a destination into an executable adventure plan.

Each experience should answer:

* Why is it worth visiting?
* Who is it best for?
* How long will it take?
* How difficult is it?
* How much will it cost?
* How far is it from the selected city?
* What should the visitor bring?
* Where should they park?
* When is the best time to go?
* Are permits or reservations required?
* Is it family-friendly?
* Is it dog-friendly?
* Is it accessible?
* What safety risks should the visitor know?
* What nearby food, lodging, rentals, or attractions can complete the day?
* What backup plan should be used if weather or access conditions change?

---

# EXECUTION DIRECTIVE

Do not produce a theoretical strategy and stop.

Work in scoped, sequenced sprints (see the Sprint Decomposition section). Do not attempt to implement all phases in a single pass. Each sprint has a defined exit condition that must be met before the next begins.

If a repository already exists, inspect the current repository, identify the technology stack, understand the existing design system, and implement the highest-value improvements directly. Do not blindly replace functioning systems. Preserve useful existing content and functionality while improving weak areas.

If no repository exists, initialize one from scratch using the stack defined in **Phase 0.5** before writing feature code.

Before making major architectural changes:

1. Inspect the project structure (or confirm none exists).
2. Identify the framework, content system, dependencies, routes, data sources, deployment setup, and design conventions.
3. Find broken, incomplete, duplicated, obsolete, or placeholder code.
4. Determine whether the current architecture can support the long-term roadmap.
5. Create a concise implementation plan.
6. Execute the plan in logical phases.
7. Test every phase.
8. Correct failures before proceeding.

When information is missing, make the safest reasonable assumption, document it, and proceed.

Do not stop merely because the project is complex. Do stop when a sprint's exit condition is met, and report before continuing.

---

# PHASE 0: LEGAL AND COMPLIANCE FOUNDATION

This phase must be completed before any feature that collects data, publishes safety information, or processes payment goes live. It is not optional and it is not deferrable.

Implement or scaffold:

* **Federal Trade Commission (FTC) affiliate disclosure** — a clear, conspicuous disclosure on every page containing affiliate links, and a standing disclosure policy page. This is legally mandatory in the United States.
* **Privacy policy** — covering data collected, cookies, analytics, email capture, and third-party processors.
* **Terms of service** — including acceptable use, intellectual property, and limitation of liability.
* **Safety liability disclaimer** — a reusable template component displayed on every adventure and guide page, stating that conditions change, that users are responsible for verifying current conditions, and that AdvnturHub is not liable for outdoor risk. Have this reviewed by a licensed attorney before launch.
* **General Data Protection Regulation (GDPR) and California Consumer Privacy Act (CCPA) baseline** — consent management for analytics and email, a data-subject request mechanism, and a cookie banner where required.
* **Digital goods tax handling** — confirm the payment processor (see Phase 0.5) collects and remits sales tax on digital products across applicable jurisdictions.

Note: I am not a licensed attorney, and this phase scaffolds compliance infrastructure rather than providing legal advice. The disclaimer, privacy policy, and terms of service must be reviewed by qualified counsel before production launch.

---

# PHASE 0.5: TECHNOLOGY STACK DECISION

Do not begin feature development until the stack is fixed. Changing it later is expensive and destabilizing. Unless the operator overrides these choices, default to:

* **Framework:** Next.js (App Router) with TypeScript
* **Database:** PostgreSQL via Supabase or Neon
* **Content Management System (CMS):** Sanity or Payload (headless)
* **Hosting and delivery:** Vercel or Cloudflare
* **Payments:** Stripe (including Stripe Tax for digital-goods compliance)
* **Email:** an established provider such as Resend, ConvertKit, or Mailchimp
* **Analytics:** a privacy-conscious tool such as Plausible or PostHog
* **Maps:** see Phase 19 for the provider decision and cost rationale

Document the final stack choice, the rationale, and any operator override in the repository README before proceeding. These choices affect hosting cost, hiring pool, content workflow, and scaling trajectory for years — treat the decision as durable.

---

# PHASE 1: REPOSITORY AND WEBSITE AUDIT (OR INITIALIZATION)

**If a repository exists,** conduct a full audit. **If none exists,** initialize the project using the Phase 0.5 stack, then treat the audit checklist below as the definition of the initial architecture to build.

Review (or scaffold):

* Directory structure
* Front-end framework
* Back-end architecture
* Content management system
* Database
* Authentication
* Existing pages
* Routing
* Components
* Styling
* Image handling
* Forms
* Search functionality
* Analytics
* SEO metadata
* Structured data
* Accessibility
* Mobile responsiveness
* Performance
* Security
* Dependencies
* Environment variables
* Build scripts
* Deployment configuration
* Broken links
* Placeholder text
* Duplicate content
* Unused code
* Missing error handling
* Console errors
* Loading states
* Empty states
* Form validation

Create an internal findings report categorized by:

* Critical
* High priority
* Medium priority
* Low priority
* Future opportunity

Then convert those findings into an implementation sequence.

---

# PHASE 2: POSITIONING AND INFORMATION ARCHITECTURE

Create a scalable website structure that supports national expansion without making the initial site feel empty.

Recommended top-level navigation:

* Explore
* Destinations
* Things to Do
* Day Trips
* Weekend Getaways
* Trip Planner
* Guides
* Shop

Include a highly visible search function.

Consider a primary call to action such as:

* Find an Adventure
* Explore Near You
* Plan My Escape
* Discover Nearby
* Build My Day Trip

Do not overcrowd the main navigation.

Use dropdowns, filters, and contextual navigation where appropriate.

## Suggested Content Hierarchy

### Explore

Allow users to discover adventures through filters such as:

* Near me
* By city
* By state
* By activity
* By season
* By travel time
* By difficulty
* By group type
* By budget
* By duration
* By accessibility
* Dog-friendly
* Family-friendly
* Free activities
* Rainy-day options

### Destinations

Structure location pages as:

* Country
* State
* Region
* Metro area
* City
* Neighborhood
* Destination
* Individual adventure

### Things to Do

Potential categories:

* Hiking
* Kayaking
* Paddleboarding
* Cycling
* Camping
* Scenic drives
* Waterfalls
* Swimming holes
* Beaches
* Caves
* Overlooks
* Parks
* Wildlife
* Museums
* Food stops
* Seasonal events
* Historic sites
* Urban exploration
* Photography locations
* Romantic activities
* Family activities

### Day Trips

Organize by:

* Departure city
* Driving time
* Activity type
* Group type
* Season
* Budget

### Weekend Getaways

Include:

* One-night escapes
* Two-night trips
* Romantic weekends
* Family weekends
* Outdoor weekends
* Budget weekends
* Luxury weekends
* Cabin trips
* Small-town escapes

### Trip Planner

Allow the visitor to generate or assemble a trip based on:

* Starting location
* Available time
* Maximum travel distance
* Budget
* Interests
* Physical ability
* Group type
* Transportation
* Desired pace
* Food preferences
* Weather
* Accessibility needs

### Guides

Include:

* Planning guides
* Packing lists
* Safety guides
* Seasonal guides
* Beginner guides
* Gear recommendations
* Destination comparisons
* Local expert interviews
* Adventure stories

### Shop

Sell:

* Downloadable itineraries
* City adventure bundles
* State adventure bundles
* Printable maps
* Packing checklists
* Notion planning templates
* Weekend escape guides
* Custom trip-planning services
* Premium memberships

---

# PHASE 3: HOMEPAGE STRATEGY

Build a homepage that immediately communicates what AdvnturHub does.

## Hero Section

The hero must include:

1. A clear, search-focused headline
2. A supporting sentence
3. A destination or activity search field
4. A primary call to action
5. Strong travel imagery
6. Optional quick filters

Potential headline directions:

* Find Your Next Adventure, Closer Than You Think
* Discover Better Day Trips and Weekend Escapes
* Turn Your Free Day Into an Adventure
* Explore Hidden Gems Near You
* Your Next Great Escape Might Be an Hour Away

Select the strongest version based on clarity, differentiation, keyword opportunity, and conversion potential.

Recommended search placeholder:

> Search a city, activity, or destination

Suggested examples beneath the search:

* Hiking near Seattle
* Day trips from Chicago
* Hidden gems near Miami
* Weekend getaways from New York City

## Homepage Sections

Build the homepage around useful discovery paths, not random content.

Recommended sections:

1. Hero and search
2. Adventures near popular cities
3. Quick escapes
4. Browse by activity
5. Browse by travel time
6. Hidden gems
7. Seasonal recommendations
8. Family, couples, solo, and dog-friendly collections
9. Featured itineraries
10. How AdvnturHub works
11. Free planning resource
12. Premium trip-planning offer
13. Latest guides
14. Email subscription
15. Trust and safety explanation
16. Footer with strong internal linking

## About Section

Use messaging similar to the following, improving it where needed:

> AdvnturHub makes it easier to discover memorable places, outdoor experiences, and short escapes without spending hours planning. From scenic day trips and hidden trails to weekend getaways and local favorites, we turn nearby possibilities into adventures you can actually take.

Add a concise brand promise:

> Less searching. More exploring.

---

# PHASE 4: SEARCH ENGINE OPTIMIZATION STRATEGY

Develop the SEO strategy around demonstrated user intent rather than forcing demand for the phrase "micro-adventure."

## Primary Keyword Categories

### Local Discovery

* Things to do near me
* Places to visit near me
* Outdoor activities near me
* Hidden gems near me
* Unique things to do near me
* Local attractions
* Nearby adventures

### Day Trips

* Best day trips from [city]
* Day trips near [city]
* One-day trips from [city]
* Weekend day-trip ideas
* Easy day trips
* Family day trips
* Romantic day trips

### Weekend Getaways

* Weekend getaways from [city]
* Weekend trips near me
* Romantic weekend getaways
* Cheap weekend getaways
* Family weekend trips
* Cabin getaways
* Small-town weekend trips

### Outdoor Activities

* Hiking trails near [city]
* Kayaking near [city]
* Waterfalls near [city]
* Scenic drives near [city]
* Swimming holes near [city]
* Beginner hiking trails
* Dog-friendly trails
* Family-friendly hikes
* Bike trails near [city]

### Hidden and Unique Places

* Hidden gems in [state]
* Secret places near [city]
* Underrated places to visit
* Unique places in [state]
* Lesser-known attractions
* Unusual things to do in [city]

### Seasonal Searches

* Fall day trips
* Best fall drives
* Spring hiking destinations
* Summer weekend getaways
* Winter cabin trips
* Christmas weekend trips
* Fall foliage near [city]
* Summer activities near me

### Audience-Specific Searches

* Things to do with kids near [city]
* Dog-friendly day trips
* Solo day-trip ideas
* Romantic things to do
* Free outdoor activities
* Accessible attractions
* Beginner outdoor adventures

---

# KEYWORD CLUSTER DELIVERABLE

Create a structured keyword map containing:

* Primary keyword
* Supporting keywords
* Search intent
* Funnel stage
* Recommended content type
* Geographic modifier
* Competition level
* Estimated traffic potential
* Monetization potential
* Suggested title
* Suggested URL
* Internal links
* Conversion opportunity

Do not invent precise search volumes unless live keyword data is available.

Clearly distinguish:

* Verified data
* Directional estimates
* Strategic assumptions

---

# PHASE 5: PROGRAMMATIC SEO ARCHITECTURE

> **Gate:** Do not activate programmatic page generation until the Content MVP Gate
> (see Sprint Decomposition) is met. Building the generator is permitted early;
> publishing generated pages before enough verified content exists creates exactly
> the index bloat and thin-content risk this phase warns against. Design the system
> now; switch it on only when the content threshold is reached.

Design the platform so it can eventually generate useful, high-quality landing pages at scale.

Potential page patterns:

* `/day-trips-from/[city]`
* `/weekend-getaways-from/[city]`
* `/things-to-do-in/[city]`
* `/things-to-do-near/[city]`
* `/hidden-gems-in/[state]`
* `/hiking-near/[city]`
* `/kayaking-near/[city]`
* `/family-adventures-near/[city]`
* `/romantic-getaways-from/[city]`
* `/dog-friendly-adventures-near/[city]`
* `/adventures-within-[time]-of/[city]`
* `/destination/[destination-name]`
* `/adventure/[adventure-name]`

Every programmatic page must provide legitimate standalone value.

Do not create thin pages by swapping city names.

Each city or category page should contain:

* Original introduction
* Curated recommendations
* Distance and travel-time information
* Map
* Filters
* Seasonal guidance
* Frequently asked questions
* Local planning information
* Supporting articles
* Relevant products or services
* Internal links
* Clear update date
* Content sourcing or editorial standards

Create safeguards against:

* Duplicate content
* Empty pages
* Keyword cannibalization
* Incorrect geographic relationships
* Outdated information
* Unverified recommendations
* Index bloat
* Low-value artificial intelligence content

A page must not be indexable until it clears a minimum-content check (verified adventures present, introduction written, map populated). Pages below threshold return `noindex` until they are complete.

---

# PHASE 6: DESTINATION AND ADVENTURE DATA MODEL

Create or improve a structured data model for every adventure.

Recommended fields:

## Identity

* Name
* Slug
* Summary
* Full description
* Destination type
* Activity categories
* Featured status

## Location

* Address
* City
* State
* Country
* Latitude
* Longitude
* Starting location
* Distance from nearby cities
* Estimated drive time

## Experience

* Duration
* Difficulty
* Elevation gain
* Route distance
* Estimated cost
* Recommended group type
* Minimum age
* Fitness level
* Skill level
* Crowd level
* Scenic rating
* Adventure rating
* Beginner suitability

## Logistics

* Parking instructions
* Parking cost
* Public transit availability
* Restroom availability
* Reservation requirements
* Permit requirements
* Operating hours
* Seasonal closures
* Accessibility information
* Cellular coverage
* Downloadable map
* Offline instructions

## Suitability

* Family-friendly
* Dog-friendly
* Couple-friendly
* Solo-friendly
* Wheelchair accessibility
* Stroller suitability
* Rainy-day suitability
* Winter suitability

## Safety

* Major hazards
* Emergency considerations
* Weather sensitivity
* Water conditions
* Wildlife warnings
* Required equipment
* Safety disclaimer
* Last verified date

## Commercial Opportunities

* Nearby restaurants
* Lodging
* Equipment rentals
* Tours
* Guides
* Gear recommendations
* Affiliate links
* Sponsored placements
* Premium itinerary availability

## Media

* Hero image
* Gallery
* Video
* Map
* Route file
* Image attribution
* Alt text

## Editorial

* Author
* Reviewer
* Sources
* Date published
* Date updated
* Last physically verified
* Confidence level

---

# PHASE 7: ADVENTURE PAGE TEMPLATE

Build an adventure page that answers practical planning questions quickly.

Recommended layout:

1. Hero image
2. Adventure name
3. Location
4. One-sentence value proposition
5. Key facts bar
6. Save, share, and map buttons
7. Overview
8. Why it is worth doing
9. Suggested itinerary
10. Route or map
11. What to bring
12. Parking and arrival instructions
13. Cost breakdown
14. Best time to visit
15. Safety and difficulty
16. Family, pet, and accessibility information
17. Nearby food and attractions
18. Alternative or backup plans
19. Frequently asked questions
20. Related adventures
21. Downloadable itinerary
22. Affiliate recommendations
23. User-submitted updates
24. Last verified date

Important practical information must appear above the fold or be easy to scan.

Every adventure page must render the Phase 0 safety liability disclaimer component.

---

# PHASE 8: CONTENT STRATEGY

Build content around search demand and trip-planning decisions.

## Content Pillars

### Destination Discovery

Examples:

* 15 Best Day Trips from Chicago
* Hidden Gems Within Two Hours of Seattle
* Best Weekend Getaways from Miami
* Unique Places to Visit Near Houston
* Scenic Drives Near Los Angeles

### Activity Discovery

Examples:

* Beginner Kayaking Destinations Near Miami
* Family-Friendly Hiking Trails Near Seattle
* Best Waterfalls Near New York City
* Dog-Friendly Adventures Near Chicago
* Best Sunset Locations Near Los Angeles

### Planning

Examples:

* How to Plan a Great Day Trip
* What to Pack for a One-Day Adventure
* How Far Should You Drive for a Day Trip?
* How to Plan an Outdoor Date
* How to Find Less-Crowded Hiking Trails

### Seasonal

Examples:

* Best Fall Day Trips from Chicago
* Summer Escapes Near Houston
* Winter Weekend Trips from New York City
* Spring Wildflower Hikes Near Los Angeles

### Commercial Content

Examples:

* Best Daypacks for Short Hikes
* Best Coolers for Road Trips
* Best Portable Chargers for Outdoor Trips
* Best Kayak Accessories for Beginners
* Best Hiking Shoes for Day Trips

Commercial content must be useful, transparent, and secondary to user trust. Every piece of commercial content must carry the FTC affiliate disclosure.

---

# PHASE 9: INITIAL DESTINATION STRATEGY

Do not launch nationwide with shallow content.

Begin with a tightly controlled set of high-opportunity metro areas.

Initial examples:

* New York City
* Chicago
* Seattle
* Los Angeles
* Miami
* Houston

Evaluate each launch city based on:

* Search demand
* Nearby destination density
* Year-round content potential
* Competition
* Affiliate opportunities
* Local partnership opportunities
* Image availability
* Ease of verifying information

For each city, create a minimum viable content cluster containing:

1. Main city adventure hub
2. Best day trips
3. Weekend getaways
4. Hidden gems
5. Hiking or outdoor activities
6. Family adventures
7. Couples adventures
8. Seasonal guide
9. At least five individual adventure pages
10. One downloadable itinerary product

Do not publish incomplete city hubs.

---

# PHASE 10: SAMPLE MICRO-ADVENTURE CONTENT

Use these initial concepts only as starting points. Verify current access, rules, safety, closures, transportation, permits, and operating conditions before publication.

### New York City

Breakneck Ridge and Cold Spring day trip

### Seattle

Rattlesnake Ledge and Rattlesnake Lake

### Los Angeles

Solstice Canyon and Malibu coastline

### Miami

Oleta River State Park kayaking and cycling

### Houston

Buffalo Bayou exploration and downtown attractions

### Chicago

Starved Rock State Park day trip

Transform each into a complete, trustworthy adventure guide using the required data model.

Do not publish outdated transportation information, unverified rental claims, inaccurate hiking distances, or unsupported safety advice.

---

# PHASE 11: MONETIZATION MODEL

Build AdvnturHub around multiple revenue streams.

## Digital Products

* Individual itineraries
* City bundles
* State bundles
* Seasonal bundles
* Family adventure packs
* Couples getaway packs
* Notion trip-planning templates
* Printable checklists
* Interactive maps
* Premium route files

Potential pricing model:

* Individual guide: $5 to $15
* City bundle: $19 to $39
* Premium regional bundle: $39 to $79
* Personalized itinerary: $75 to $300
* Membership: $7 to $15 per month or $59 to $129 per year

Treat these as strategic starting ranges, not rigid requirements.

> **Scope warning:** Selling digital products is a second product, not a feature.
> A functioning shop requires payment processing, secure file hosting, digital
> delivery, customer authentication, purchase history, refund handling, failed-payment
> recovery, and multi-jurisdiction digital-goods tax compliance. Treat the Shop as its
> own dedicated build sprint with its own acceptance criteria. Do not bolt it onto an
> unrelated sprint.

## Affiliate Revenue

Potential categories:

* Hotels
* Vacation rentals
* Tours
* Equipment rentals
* Outdoor gear
* Travel insurance
* Car rentals
* Attractions
* Experiences
* Camping reservations
* Outdoor classes

Do not build the business around a single affiliate program. All affiliate placements require FTC disclosure (Phase 0).

## Sponsorships

Potential partners:

* Tourism boards
* Local outfitters
* Restaurants
* Hotels
* Chambers of commerce
* Recreation companies
* Event organizers
* Outdoor brands

Clearly label sponsored content.

## Premium Membership

Potential benefits:

* Full itinerary library
* Downloadable maps
* Offline access
* Personalized recommendations
* Exclusive hidden-gem guides
* Seasonal collections
* Discounts
* Trip-planning tools
* Saved trips
* Alerts for new adventures

---

# PHASE 12: CUSTOM TRIP-PLANNING OFFER

Replace weak wording such as:

> Get a custom trip from us for money.

Use stronger positioning.

Recommended title:

> Your Adventure, Built Around You

Recommended description:

> Tell us where you are starting, how much time you have, and what kind of experience you want. We will create a personalized adventure plan with destinations, timing, activities, food stops, maps, and practical details.

Create:

* Service landing page
* Intake questionnaire
* Pricing structure
* Delivery timeline
* Scope boundaries
* Revision policy
* Payment process
* Automated confirmation
* Customer dashboard or secure delivery method
* Upsells
* Refund policy
* Frequently asked questions

Suggested intake fields:

* Starting location
* Date
* Number of travelers
* Ages
* Budget
* Maximum driving time
* Interests
* Fitness level
* Accessibility needs
* Pet requirements
* Food preferences
* Desired pace
* Lodging preference
* Non-negotiables
* Activities to avoid

---

# PHASE 13: CONVERSION SYSTEM

Build a clear visitor journey.

## First-Time Visitor

1. Searches a city or activity
2. Finds a relevant collection
3. Reviews practical recommendations
4. Saves an adventure
5. Downloads a free planning resource
6. Joins the email list
7. Purchases an itinerary or clicks a relevant partner link

## Returning Visitor

1. Receives location-specific recommendations
2. Views saved adventures
3. Builds a trip
4. Purchases a bundle or membership
5. Shares the completed adventure
6. Submits a review or update

## Calls to Action

Use clear calls to action such as:

* Find Adventures Near Me
* Explore This Route
* Save This Adventure
* Build My Day Trip
* Download the Itinerary
* View the Map
* Plan a Custom Escape
* See Weekend Ideas
* Get Local Recommendations

Avoid generic buttons such as:

* Learn More
* Click Here
* Submit

Use generic language only where context makes the action obvious.

---

# PHASE 14: EMAIL MARKETING

Create a lead-generation and nurturing system.

## Lead Magnets

Examples:

* 25 Adventures Within Two Hours of Your City
* The Ultimate Day-Trip Packing List
* Weekend Escape Planner
* Hidden Gems Near [City]
* One-Day Adventure Planning Template

## Welcome Sequence

Email 1: Deliver the resource and establish the brand promise

Email 2: Help the subscriber choose the right type of adventure

Email 3: Showcase a local itinerary

Email 4: Explain how AdvnturHub saves planning time

Email 5: Present a relevant paid guide or membership

## Ongoing Email Content

* Weekend recommendations
* Seasonal adventures
* Newly added destinations
* Weather-appropriate ideas
* Limited-time local events
* Destination bundles
* User stories
* Gear and planning guidance

Segment subscribers by:

* Location
* Interests
* Family status
* Preferred activities
* Travel distance
* Purchase history
* Engagement

All email capture requires explicit consent and a documented lawful basis under GDPR/CCPA (Phase 0).

---

# PHASE 15: SOCIAL MEDIA STRATEGY

Create content that markets the outcome, not the terminology.

Do not rely on "micro-adventure" as the hook.

Use concepts such as:

* Three places you can visit this weekend
* Hidden destinations within an hour of the city
* A complete day trip for under $100
* Leave at 8:00 a.m., return by dinner
* What to do when you need to get out of the city
* The best local adventure nobody talks about
* A one-day itinerary from start to finish
* Date ideas better than another restaurant
* Family adventures that do not require a plane ticket
* Scenic drives worth the mileage

## Short-Form Video Structure

1. Strong visual hook
2. Location and travel time
3. Why it is worth visiting
4. One practical planning detail
5. Clear action

Example:

> Only 90 minutes from Chicago, this canyon trail feels nothing like Illinois. Here is exactly where to park, which route to take, and when to arrive before the crowds.

Create reusable templates for:

* Instagram Reels
* TikTok
* YouTube Shorts
* Pinterest
* Facebook
* Email
* Blog distribution

---

# PHASE 16: LOCAL PARTNERSHIP SYSTEM

Create a repeatable process for identifying and recruiting:

* Tour operators
* Kayak rental companies
* Bike rental businesses
* Local guides
* Restaurants
* Hotels
* Campgrounds
* Tourism offices
* Event companies
* Photographers
* Outdoor stores

Build:

* Partner landing page
* Partnership inquiry form
* Media kit
* Sponsored listing guidelines
* Affiliate tracking process
* Outreach templates
* Partner onboarding
* Quality standards
* Disclosure requirements
* Reporting dashboard

Partners must not be allowed to purchase falsely positive editorial coverage.

---

# PHASE 17: DESIGN SYSTEM

Build a consistent design system.

Include:

* Typography scale
* Spacing system
* Button hierarchy
* Form styles
* Card components
* Filters
* Tags
* Badges
* Map markers
* Difficulty indicators
* Price indicators
* Duration indicators
* Responsive breakpoints
* Image ratios
* Loading skeletons
* Empty states
* Error states
* Accessibility states

The visual direction should combine:

* Large, immersive travel imagery
* Strong readability
* Clean white space
* Earth-inspired accents
* High-contrast calls to action
* Modern cards
* Clear filtering
* Mobile-first interaction

Do not use visual effects that reduce speed, readability, or accessibility.

---

# PHASE 18: SEARCH AND FILTERING

Build a useful search system.

Search should support:

* City
* State
* Destination name
* Activity
* Adventure type
* Keyword
* Nearby location

Filters should include:

* Distance
* Driving time
* Duration
* Difficulty
* Cost
* Activity
* Season
* Group type
* Family-friendly
* Dog-friendly
* Accessibility
* Indoor or outdoor
* Free or paid
* Reservation required
* Crowd level

Include:

* Useful empty-state suggestions
* Clear filter reset
* Search result count
* Sort options
* Mobile filter drawer
* Shareable filtered URLs
* Fast performance
* Keyboard accessibility

---

# PHASE 19: MAP EXPERIENCE

Build or prepare the architecture for an interactive map.

**Provider decision (make this explicitly before building):**

* **Mapbox** — generous free tier suitable for an early-stage product; recommended default.
* **MapLibre with OpenStreetMap** — free and open-source, no per-call cost, but more implementation effort. Best long-term cost profile.
* **Google Maps Platform** — richest data, but charges per Application Programming Interface (API) call and becomes expensive at meaningful traffic. Choose only if a specific feature requires it.

Default to Mapbox for launch and design the map layer so the provider can be swapped without rewriting page logic. Document the choice and the cost assumptions in the README.

Potential capabilities:

* Search an area
* View adventure pins
* Filter visible results
* Cluster nearby markers
* Open preview cards
* Save destinations
* Build a route
* Display drive times
* Show nearby food, lodging, and rentals
* Switch between map and list view
* Share a map
* Download an itinerary

Protect costs by considering:

* Map provider pricing
* Request limits
* Caching
* Lazy loading
* Static map previews
* Geocoding usage
* Routing usage

Do not expose private application programming interface keys.

---

# PHASE 20: TECHNICAL SEO

Implement:

* Unique title tags
* Strong meta descriptions
* Canonical URLs
* XML sitemap
* Robots directives
* Breadcrumbs
* Open Graph metadata
* Social preview images
* Structured data
* Semantic heading hierarchy
* Optimized internal linking
* Image alt text
* Image compression
* Responsive images
* Fast page rendering
* Pagination controls
* Redirect management
* Broken-link detection
* Indexation controls
* Duplicate-content safeguards

Potential structured data types:

* Organization
* WebSite
* BreadcrumbList
* Article
* TouristAttraction
* Place
* Trip
* ItemList
* FAQPage, only when permitted and appropriate
* Product
* Offer
* Review, only with legitimate reviews

Never add misleading structured data.

---

# PHASE 21: TRUST, SAFETY, AND CONTENT QUALITY

Travel information can become outdated and can create real safety risks.

Every guide should display:

* Last updated date
* Verification status
* Source information
* Safety notice
* Weather sensitivity
* Seasonal access notes
* Official resource links
* Emergency guidance where appropriate

Create a content verification workflow.

Verification levels:

1. Firsthand verified
2. Confirmed through official sources
3. Confirmed through multiple reputable secondary sources
4. Community submitted and awaiting verification

Do not represent unverified content as firsthand experience.

Create a method for users to report:

* Closures
* Incorrect directions
* Unsafe conditions
* Pricing changes
* Permit changes
* Accessibility changes
* Business closures
* Seasonal issues

---

# PHASE 22: ACCESSIBILITY

Meet or exceed Web Content Accessibility Guidelines (WCAG) 2.2 Level AA where reasonably possible.

Include:

* Keyboard navigation
* Visible focus states
* Semantic HTML
* Adequate contrast
* Descriptive labels
* Alternative text
* Accessible forms
* Accessible modals
* Reduced-motion support
* Screen-reader-friendly filters
* Proper heading order
* Accessible error messages

Test critical workflows with keyboard-only navigation.

---

# PHASE 23: PERFORMANCE

Optimize for Core Web Vitals.

Focus on:

* Largest Contentful Paint
* Interaction to Next Paint
* Cumulative Layout Shift

Implement:

* Image optimization
* Lazy loading
* Code splitting
* Font optimization
* Caching
* Minification
* Server-side rendering or static generation where appropriate
* Limited third-party scripts
* Efficient database queries
* Loading states
* Mobile performance

Do not sacrifice usability for decorative animation.

---

# PHASE 24: ANALYTICS AND MEASUREMENT

Implement privacy-conscious analytics.

Track:

* Search queries
* Search result clicks
* Filter usage
* Adventure saves
* Map interactions
* Itinerary downloads
* Email signups
* Product purchases
* Affiliate clicks
* Custom trip inquiries
* Membership conversion
* Scroll depth
* Exit pages
* Internal search failures
* City-level demand
* Content engagement

Create an event naming system.

Define a basic reporting dashboard with:

* Organic traffic
* Top landing pages
* Conversion rate
* Revenue by source
* Revenue by city
* Email growth
* Affiliate click-through rate
* Product conversion rate
* Returning visitors
* Most requested locations
* Content gaps

Do not track unnecessary sensitive information. Analytics must respect the consent mechanism defined in Phase 0.

---

# PHASE 25: ADMINISTRATIVE WORKFLOW

Create or improve the administrative content workflow.

The administrator should be able to:

* Add an adventure
* Edit an adventure
* Add destinations
* Upload images
* Add map coordinates
* Assign activities
* Set suitability attributes
* Add affiliate links
* Add safety warnings
* Set verification status
* Schedule publication
* Update seasonal access
* Mark a location temporarily closed
* Add related content
* Generate a preview
* Review SEO fields
* View content quality warnings

Include validation that prevents publication when critical fields are missing.

---

# PHASE 26: TESTING

Create and run an appropriate test strategy.

Include:

* Unit tests
* Integration tests
* End-to-end tests
* Responsive tests
* Accessibility tests
* Link tests
* Form tests
* Search tests
* Filter tests
* Checkout tests
* Authentication tests, if applicable
* Metadata tests
* Structured data validation
* Performance checks
* Security checks

Test at minimum:

* Homepage
* Search
* City page
* Adventure page
* Article page
* Product page
* Custom trip form
* Email signup
* Checkout
* Mobile menu
* Filters
* Error pages

Do not claim something works unless it has been tested or clearly label it as untested.

---

# PHASE 27: SECURITY

Review and improve:

* Environment variable handling
* Authentication
* Authorization
* Input validation
* Form sanitization
* Cross-site scripting protection
* Cross-site request forgery protection
* Rate limiting
* File uploads
* Dependency vulnerabilities
* Secret exposure
* Payment handling
* Administrative access
* Error messages
* Logging
* Backups

Never commit secrets, private keys, credentials, or production tokens.

---

# PHASE 28: REQUIRED DELIVERABLES

Produce and implement, where the repository supports it:

1. Legal and compliance foundation (Phase 0)
2. Documented technology stack decision (Phase 0.5)
3. Repository audit or initialization
4. Prioritized build plan
5. Updated information architecture
6. Improved homepage
7. Responsive navigation
8. Search experience
9. Destination page template
10. Adventure page template
11. Article template
12. Product or itinerary page
13. Custom trip-planning page
14. Email capture system
15. Structured adventure data model
16. SEO metadata system
17. Structured data
18. Sitemap and robots configuration
19. Internal linking system
20. Initial city content architecture
21. Analytics event plan
22. Accessibility improvements
23. Performance improvements
24. Testing suite
25. Documentation
26. Launch checklist
27. Post-launch roadmap

---

# SPRINT DECOMPOSITION

The 28 phases cannot be executed in a single pass. Break them into sequenced sprints, each with a defined exit condition. Do not begin a sprint until the previous sprint's exit condition is met.

### Sprint 1 — Foundation
Phases 0, 0.5, 1. **Exit condition:** legal/compliance scaffolding in place, stack chosen and documented, repository initialized and building cleanly.

### Sprint 2 — Core Experience
Phases 2, 3, 17, 18. **Exit condition:** design system, responsive navigation, homepage, and working search render and pass accessibility and responsive tests.

### Sprint 3 — Content Templates and First City
Phases 6, 7, 9 (one city), 21, 22. **Exit condition:** the adventure data model and page template are complete; one full city hub with at least five verified adventure pages is published; safety disclaimers render.

### Sprint 4 — Content MVP Gate
Phases 8, 9 (remaining launch cities), 10. **Exit condition — the Content MVP Gate:** at least 30 verified adventures across five cities, each meeting the full Phase 6 data model. **Programmatic SEO (Phase 5) must not publish generated pages until this gate is cleared.**

### Sprint 5 — Programmatic SEO and Technical SEO
Phases 5 (activated), 20. **Exit condition:** programmatic pages generate only from verified content, thin pages return `noindex`, sitemap and structured data validate.

### Sprint 6 — Commerce
Phases 11 (Shop), 12, 13. **Exit condition:** payment, digital delivery, refunds, and tax handling tested end-to-end; custom trip-planning flow functional. Treat the Shop as its own build with its own acceptance criteria.

### Sprint 7 — Growth Systems
Phases 14, 15, 16, 24, 25. **Exit condition:** email capture with consent, analytics events firing, admin workflow validated.

### Sprint 8 — Hardening and Launch
Phases 23, 26, 27, plus the launch checklist. **Exit condition:** performance, testing, and security review complete; no critical or high-priority defect open.

---

# SELF-CORRECTING EXECUTION LOOP

Use the following loop throughout each sprint.

## Step 1: Inspect

Review the relevant files, architecture, requirements, and dependencies.

## Step 2: Diagnose

Identify:

* What exists
* What is missing
* What is broken
* What creates risk
* What produces the highest business value

## Step 3: Plan

Choose the smallest logical implementation that supports the long-term architecture.

## Step 4: Build

Implement clean, maintainable, production-quality code.

## Step 5: Test

Run all relevant tests, checks, builds, and validations.

## Step 6: Critique

Act as a hostile reviewer.

Ask:

* Is the experience obvious?
* Is the code maintainable?
* Is the content useful?
* Is the page fast?
* Is it accessible?
* Is it trustworthy?
* Does it support search intent?
* Does it produce a clear conversion path?
* Does it create future technical debt?
* Is any claim unverified?
* Would a real traveler confidently use this?

## Step 7: Repair

Correct every material issue found.

## Step 8: Re-Test

Repeat testing after repairs.

## Step 9: Document

Record:

* What changed
* Why it changed
* What assumptions were made
* What remains incomplete
* What should happen next

Continue the loop until the sprint's exit condition is satisfied or an external dependency genuinely prevents completion.

Do not accept "good enough" when an obvious defect remains.

---

# ANTI-HALLUCINATION RULES

Never fabricate:

* Search volume
* Customer testimonials
* Firsthand visits
* Trail conditions
* Prices
* Business hours
* Permits
* Accessibility
* Transportation schedules
* Safety claims
* Affiliate relationships
* User reviews
* Geographic distances
* Operating status

When live data is unavailable:

1. Mark the field as requiring verification.
2. Build the system so the correct data can be added.
3. Do not fill the interface with invented information.

---

# DECISION-MAKING RULES

When several solutions are possible, prioritize in this order:

1. Legal and regulatory compliance
2. User safety
3. Accuracy
4. User clarity
5. Search intent
6. Mobile usability
7. Performance
8. Accessibility
9. Maintainability
10. Conversion potential
11. Visual polish

Challenge requests that would damage trust, security, usability, legal standing, or long-term growth.

Do not agree with a flawed approach merely because it was suggested.

Explain the issue internally, select the superior solution, and proceed.

---

# DEFINITION OF DONE

The project is not complete merely because pages render.

A feature is complete only when:

* It works
* It is responsive
* It is accessible
* It handles loading and error states
* It is tested
* It is documented
* It uses accurate data
* It follows the design system
* It supports the intended search intent
* It has a clear user action
* It complies with the Phase 0 legal and compliance requirements
* It does not create obvious security or performance problems

---

# FINAL REPORT FORMAT

At the end of each working session, provide:

## 1. Executive Summary

Explain what was built and the business value created.

## 2. Completed Work

List completed changes by area.

## 3. Files Changed

List the primary files created, modified, or removed.

## 4. Tests and Validation

Report:

* Tests run
* Build results
* Accessibility checks
* Performance checks
* Known limitations

## 5. Assumptions

Document every material assumption.

## 6. Remaining Risks

State unresolved problems directly.

## 7. Recommended Next Actions

Rank the next actions by:

* Priority
* Expected impact
* Effort
* Dependency

## 8. Launch Readiness

Give one status:

* Not ready
* Development ready
* Staging ready
* Production ready

Do not declare production readiness when material tests, content verification, legal review, payment configuration, security review, or deployment validation remain incomplete.

---

# STARTING INSTRUCTION

Begin with Sprint 1.

1. If a repository exists, inspect it fully before modifying code. If none exists, confirm the Phase 0.5 stack and initialize the project.
2. Complete Phase 0 (legal and compliance scaffolding) and Phase 0.5 (documented stack decision) before feature work.
3. Summarize the current state.
4. Identify the most important problems.
5. Confirm the sprint plan.
6. Begin executing Sprint 1 through the self-correcting loop.
7. Stop at the sprint exit condition and report before continuing.
8. Leave the repository in a cleaner, more functional, and more scalable condition than you found it.

The final product must position AdvnturHub as the trusted answer to:

> "What should I do with my free day?"
