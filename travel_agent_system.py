"""
=============================================================================
  KNOWLEDGE REPRESENTATION MODEL — Travel Agency (Client Interaction)
  Course: Artificial Intelligence in Robotics
=============================================================================
  Approaches used:
    1. Frame / Class-based  → Entities: Client, Destination, TravelPackage, Booking
    2. Rule-based System    → IF-THEN rules for recommendations & validation
    3. Knowledge Graph      → Semantic network of relationships between entities
=============================================================================
"""

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: FRAME / CLASS-BASED REPRESENTATION
# Represents real-world entities as structured frames (classes with attributes)
# ─────────────────────────────────────────────────────────────────────────────

class Client:
    """Frame representing a travel agency client."""
    def __init__(self, client_id, name, age, budget, preferences, travel_history=None):
        self.client_id    = client_id
        self.name         = name
        self.age          = age
        self.budget       = budget          # in USD
        self.preferences  = preferences     # list, e.g. ["beach", "adventure", "culture"]
        self.travel_history = travel_history or []  # list of visited destination codes

    def __repr__(self):
        return f"Client({self.name}, budget=${self.budget}, prefs={self.preferences})"


class Destination:
    """Frame representing a travel destination."""
    def __init__(self, code, name, country, climate, tags, avg_cost_per_day, visa_required=False):
        self.code             = code
        self.name             = name
        self.country          = country
        self.climate          = climate          # "tropical", "cold", "temperate", "arid"
        self.tags             = tags             # e.g. ["beach", "culture", "adventure"]
        self.avg_cost_per_day = avg_cost_per_day # in USD
        self.visa_required    = visa_required

    def __repr__(self):
        return f"Destination({self.name}, {self.country}, ~${self.avg_cost_per_day}/day)"


class TravelPackage:
    """Frame representing a travel package offered by the agency."""
    def __init__(self, pkg_id, name, destination_code, duration_days, total_price,
                 includes_hotel, includes_flight, category):
        self.pkg_id          = pkg_id
        self.name            = name
        self.destination_code = destination_code
        self.duration_days   = duration_days
        self.total_price     = total_price
        self.includes_hotel  = includes_hotel
        self.includes_flight = includes_flight
        self.category        = category  # "budget", "standard", "luxury"

    def __repr__(self):
        return f"Package({self.name}, ${self.total_price}, {self.duration_days} days)"


class Booking:
    """Frame representing a client booking."""
    def __init__(self, booking_id, client_id, pkg_id, travel_date, status="pending"):
        self.booking_id  = booking_id
        self.client_id   = client_id
        self.pkg_id      = pkg_id
        self.travel_date = travel_date
        self.status      = status   # "pending", "confirmed", "cancelled"

    def __repr__(self):
        return f"Booking({self.booking_id}, client={self.client_id}, pkg={self.pkg_id}, {self.status})"


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: KNOWLEDGE BASE (Facts)
# The agency's stored knowledge about destinations and packages
# ─────────────────────────────────────────────────────────────────────────────

class KnowledgeBase:
    """Stores all known facts about destinations, packages, clients, bookings."""

    def __init__(self):
        self.destinations = {}   # code -> Destination
        self.packages     = {}   # pkg_id -> TravelPackage
        self.clients      = {}   # client_id -> Client
        self.bookings     = {}   # booking_id -> Booking

    # --- Add facts ---
    def add_destination(self, dest: Destination):
        self.destinations[dest.code] = dest

    def add_package(self, pkg: TravelPackage):
        self.packages[pkg.pkg_id] = pkg

    def add_client(self, client: Client):
        self.clients[client.client_id] = client

    def add_booking(self, booking: Booking):
        self.bookings[booking.booking_id] = booking

    # --- Query facts ---
    def get_packages_for_destination(self, dest_code):
        return [p for p in self.packages.values() if p.destination_code == dest_code]

    def get_client_bookings(self, client_id):
        return [b for b in self.bookings.values() if b.client_id == client_id]


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: RULE-BASED SYSTEM
# IF-THEN inference rules for client recommendations and booking validation
# ─────────────────────────────────────────────────────────────────────────────

class RuleEngine:
    """
    Rule-based inference engine for travel agency decisions.

    Rules implemented:
      R1 — Recommend destinations matching client preferences
      R2 — Filter packages within client budget
      R3 — Avoid destinations client has already visited
      R4 — Flag visa requirements for client awareness
      R5 — Recommend package category based on budget level
      R6 — Validate a booking (budget check + package existence)
    """

    def __init__(self, kb: KnowledgeBase):
        self.kb = kb

    def recommend_destinations(self, client: Client):
        """R1 + R3: Match preferences, exclude already-visited."""
        matched = []
        for dest in self.kb.destinations.values():
            # R1: at least one preference tag matches destination tags
            if any(pref in dest.tags for pref in client.preferences):
                # R3: exclude already visited
                if dest.code not in client.travel_history:
                    matched.append(dest)
        return matched

    def filter_packages_by_budget(self, client: Client, destinations):
        """R2: Keep packages whose total price fits client budget."""
        dest_codes = {d.code for d in destinations}
        affordable = []
        for pkg in self.kb.packages.values():
            if pkg.destination_code in dest_codes and pkg.total_price <= client.budget:
                affordable.append(pkg)
        return affordable

    def recommend_category(self, client: Client):
        """R5: Suggest package tier based on budget."""
        if client.budget < 1500:
            return "budget"
        elif client.budget < 4000:
            return "standard"
        else:
            return "luxury"

    def check_visa_warnings(self, client: Client, destinations):
        """R4: Warn if any recommended destination requires a visa."""
        warnings = []
        for dest in destinations:
            if dest.visa_required:
                warnings.append(
                    f"⚠ Visa required for {dest.name} ({dest.country}). "
                    f"Please ensure {client.name} has valid documentation."
                )
        return warnings

    def validate_booking(self, client: Client, pkg: TravelPackage):
        """R6: Validate whether a booking can proceed."""
        issues = []
        if pkg.pkg_id not in self.kb.packages:
            issues.append("Package does not exist in the knowledge base.")
        if client.budget < pkg.total_price:
            issues.append(
                f"Client budget (${client.budget}) is less than package price (${pkg.total_price})."
            )
        if not issues:
            return True, "Booking is valid. Ready to confirm."
        return False, " | ".join(issues)

    def full_recommendation(self, client: Client):
        """Run all rules and return a structured recommendation report."""
        print(f"\n{'='*60}")
        print(f"  RECOMMENDATION REPORT FOR: {client.name.upper()}")
        print(f"  Budget: ${client.budget} | Preferences: {client.preferences}")
        print(f"{'='*60}")

        # Apply rules
        matched_dests = self.recommend_destinations(client)
        affordable_pkgs = self.filter_packages_by_budget(client, matched_dests)
        category = self.recommend_category(client)
        visa_warnings = self.check_visa_warnings(client, matched_dests)

        print(f"\n[R1+R3] Recommended Destinations ({len(matched_dests)} found):")
        for d in matched_dests:
            print(f"   → {d.name}, {d.country}  | Tags: {d.tags} | ~${d.avg_cost_per_day}/day")

        print(f"\n[R2]    Affordable Packages (within ${client.budget}):")
        if affordable_pkgs:
            for p in affordable_pkgs:
                dest = self.kb.destinations.get(p.destination_code)
                dest_name = dest.name if dest else p.destination_code
                print(f"   → [{p.category.upper()}] {p.name} to {dest_name} — "
                      f"${p.total_price} for {p.duration_days} days")
        else:
            print("   (No affordable packages found)")

        print(f"\n[R5]    Suggested Package Category: {category.upper()}")

        if visa_warnings:
            print(f"\n[R4]    Visa Warnings:")
            for w in visa_warnings:
                print(f"   {w}")

        return affordable_pkgs


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4: KNOWLEDGE GRAPH (Semantic Network)
# Represents relationships between entities as a directed graph
# ─────────────────────────────────────────────────────────────────────────────

class KnowledgeGraph:
    """
    Semantic network storing (subject, relation, object) triples.

    Example triples:
      ("client:C001", "PREFERS", "tag:beach")
      ("package:PKG1", "GOES_TO", "destination:MALDIVES")
      ("client:C001", "BOOKED", "package:PKG1")
      ("destination:MALDIVES", "IS_IN", "country:Maldives")
    """

    def __init__(self):
        self.triples = []   # list of (subject, relation, object)
        self.index   = {}   # subject -> list of (relation, object)

    def add_triple(self, subject, relation, obj):
        triple = (subject, relation, obj)
        self.triples.append(triple)
        if subject not in self.index:
            self.index[subject] = []
        self.index[subject].append((relation, obj))

    def query(self, subject=None, relation=None, obj=None):
        """Retrieve triples matching any combination of s/r/o."""
        results = []
        for s, r, o in self.triples:
            if (subject  is None or s == subject)  and \
               (relation is None or r == relation) and \
               (obj      is None or o == obj):
                results.append((s, r, o))
        return results

    def get_relations(self, subject):
        """All relations and objects for a given subject."""
        return self.index.get(subject, [])

    def populate_from_kb(self, kb: KnowledgeBase):
        """Auto-generate triples from the knowledge base facts."""
        for dest in kb.destinations.values():
            node = f"destination:{dest.code}"
            self.add_triple(node, "IS_IN",    f"country:{dest.country}")
            self.add_triple(node, "HAS_CLIMATE", f"climate:{dest.climate}")
            for tag in dest.tags:
                self.add_triple(node, "TAGGED_AS", f"tag:{tag}")
            if dest.visa_required:
                self.add_triple(node, "REQUIRES", "document:visa")

        for pkg in kb.packages.values():
            node = f"package:{pkg.pkg_id}"
            self.add_triple(node, "GOES_TO",   f"destination:{pkg.destination_code}")
            self.add_triple(node, "CATEGORY",  f"category:{pkg.category}")
            self.add_triple(node, "COSTS",     f"price:{pkg.total_price}USD")
            if pkg.includes_flight:
                self.add_triple(node, "INCLUDES", "service:flight")
            if pkg.includes_hotel:
                self.add_triple(node, "INCLUDES", "service:hotel")

        for client in kb.clients.values():
            node = f"client:{client.client_id}"
            for pref in client.preferences:
                self.add_triple(node, "PREFERS", f"tag:{pref}")
            for visited in client.travel_history:
                self.add_triple(node, "VISITED", f"destination:{visited}")

        for booking in kb.bookings.values():
            node = f"booking:{booking.booking_id}"
            self.add_triple(node, "MADE_BY",   f"client:{booking.client_id}")
            self.add_triple(node, "INCLUDES",  f"package:{booking.pkg_id}")
            self.add_triple(node, "STATUS",    f"status:{booking.status}")
            # Also link client → booking
            self.add_triple(f"client:{booking.client_id}", "HAS_BOOKING", node)

    def print_graph(self, filter_subject=None):
        print(f"\n{'='*60}")
        print(f"  KNOWLEDGE GRAPH TRIPLES" +
              (f" for {filter_subject}" if filter_subject else ""))
        print(f"{'='*60}")
        triples = self.query(subject=filter_subject) if filter_subject else self.triples
        for s, r, o in triples:
            print(f"  ({s})  --[{r}]-->  ({o})")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5: DEMO — Putting it all together
# ─────────────────────────────────────────────────────────────────────────────

def build_demo_knowledge_base():
    kb = KnowledgeBase()

    # --- Destinations ---
    kb.add_destination(Destination("MALDIVES",  "Maldives",       "Maldives",     "tropical",  ["beach", "luxury", "relaxation"], 350, visa_required=False))
    kb.add_destination(Destination("PARIS",     "Paris",          "France",       "temperate", ["culture", "romance", "history"], 200, visa_required=False))
    kb.add_destination(Destination("NEPAL",     "Kathmandu",      "Nepal",        "cold",      ["adventure", "trekking", "culture"], 80,  visa_required=True))
    kb.add_destination(Destination("BALI",      "Bali",           "Indonesia",    "tropical",  ["beach", "culture", "adventure"], 120, visa_required=False))
    kb.add_destination(Destination("DUBAI",     "Dubai",          "UAE",          "arid",      ["luxury", "shopping", "culture"], 300, visa_required=True))
    kb.add_destination(Destination("PATAGONIA", "Patagonia",      "Argentina",    "cold",      ["adventure", "nature", "trekking"], 150, visa_required=False))

    # --- Packages ---
    kb.add_package(TravelPackage("PKG1", "Bali Bliss",         "BALI",      7,  1200, True,  True,  "budget"))
    kb.add_package(TravelPackage("PKG2", "Paris Romance",      "PARIS",     5,  2500, True,  True,  "standard"))
    kb.add_package(TravelPackage("PKG3", "Maldives Escape",    "MALDIVES",  6,  5500, True,  True,  "luxury"))
    kb.add_package(TravelPackage("PKG4", "Nepal Trek",         "NEPAL",     10, 1800, True,  True,  "standard"))
    kb.add_package(TravelPackage("PKG5", "Dubai Luxury",       "DUBAI",     4,  4200, True,  True,  "luxury"))
    kb.add_package(TravelPackage("PKG6", "Patagonia Wild",     "PATAGONIA", 12, 3200, True,  True,  "standard"))
    kb.add_package(TravelPackage("PKG7", "Bali Budget Stay",   "BALI",      5,  750,  False, True,  "budget"))

    # --- Clients ---
    kb.add_client(Client("C001", "Alice Johnson", 30, 2000, ["beach", "adventure"], travel_history=["BALI"]))
    kb.add_client(Client("C002", "Bob Smith",     45, 6000, ["luxury", "culture", "romance"]))
    kb.add_client(Client("C003", "Clara Lee",     25, 1300, ["adventure", "trekking", "nature"]))

    # --- Bookings ---
    kb.add_booking(Booking("B001", "C002", "PKG3", "2025-07-15", status="confirmed"))

    return kb


def main():
    print("\n" + "█"*62)
    print("   TRAVEL AGENCY — AI Knowledge Representation System")
    print("   Course: Artificial Intelligence in Robotics")
    print("█"*62)

    # Build the knowledge base
    kb = KnowledgeBase()
    kb = build_demo_knowledge_base()

    # Build the knowledge graph from KB facts
    kg = KnowledgeGraph()
    kg.populate_from_kb(kb)

    # Instantiate the rule engine
    engine = RuleEngine(kb)

    # ── Demo 1: Recommendation for Alice (budget traveler, beach/adventure) ──
    alice = kb.clients["C001"]
    alice_packages = engine.full_recommendation(alice)

    # ── Demo 2: Recommendation for Bob (luxury traveler) ──
    bob = kb.clients["C002"]
    engine.full_recommendation(bob)

    # ── Demo 3: Recommendation for Clara (budget, adventure/trekking) ──
    clara = kb.clients["C003"]
    engine.full_recommendation(clara)

    # ── Demo 4: Booking validation ──
    print(f"\n{'='*60}")
    print("  BOOKING VALIDATION")
    print(f"{'='*60}")

    # Alice tries to book Maldives Escape (too expensive)
    pkg_maldives = kb.packages["PKG3"]
    valid, msg = engine.validate_booking(alice, pkg_maldives)
    print(f"\n  Alice → Maldives Escape:  {'✓' if valid else '✗'}  {msg}")

    # Alice tries to book Bali Budget Stay (affordable)
    pkg_bali = kb.packages["PKG7"]
    valid, msg = engine.validate_booking(alice, pkg_bali)
    print(f"  Alice → Bali Budget Stay: {'✓' if valid else '✗'}  {msg}")

    # ── Demo 5: Knowledge Graph queries ──
    kg.print_graph(filter_subject="client:C001")
    kg.print_graph(filter_subject="package:PKG4")

    # Semantic query: which destinations require a visa?
    print(f"\n{'='*60}")
    print("  GRAPH QUERY: Destinations requiring a visa")
    print(f"{'='*60}")
    visa_triples = kg.query(relation="REQUIRES", obj="document:visa")
    for s, r, o in visa_triples:
        print(f"   → {s}")

    # Semantic query: what does Bob prefer?
    print(f"\n{'='*60}")
    print("  GRAPH QUERY: Bob's preferences (client:C002)")
    print(f"{'='*60}")
    bob_prefs = kg.query(subject="client:C002", relation="PREFERS")
    for s, r, o in bob_prefs:
        print(f"   → {o}")

    print(f"\n{'='*60}")
    print("  END OF DEMO")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()