# ---------------------------------------------------------------
#   KNOWLEDGE REPRESENTATION SYSTEM - TRAVEL AGENCY
#   Subject Area : Working with Clients (Business Travelers)
#   Author       : Your Name
#   Mentor       : Claude (Anthropic)
#   Version      : Final - Steps 1 through 6 Complete
# ---------------------------------------------------------------


# ---------------------------------------------------------------
# SECTION 1: CORE ENTITIES (Ontology)
# ---------------------------------------------------------------

class Destination:
    """Represents a travel destination and its properties."""

    def __init__(self, name, country, climate, visa_required, avg_cost_per_day, tags):
        self.name = name
        self.country = country
        self.climate = climate
        self.visa_required = visa_required
        self.avg_cost_per_day = avg_cost_per_day
        self.tags = tags

    def __repr__(self):
        return f"Destination({self.name}, {self.country})"


class TravelPackage:
    """Represents a bundled travel offer (flight + hotel + services)."""

    def __init__(self, package_id, name, destination, price, duration_days, services, travel_class):
        self.package_id = package_id
        self.name = name
        self.destination = destination
        self.price = price
        self.duration_days = duration_days
        self.services = services
        self.travel_class = travel_class

    def __repr__(self):
        return f"Package({self.name}, ${self.price}, {self.duration_days} days)"


class Client:
    """Represents a travel agency client."""

    def __init__(self, client_id, name, age, budget, travel_type, preferences, loyalty_tier="standard"):
        self.client_id = client_id
        self.name = name
        self.age = age
        self.budget = budget
        self.travel_type = travel_type
        self.preferences = preferences
        self.loyalty_tier = loyalty_tier
        self.booking_history = []

    def __repr__(self):
        return f"Client({self.name}, budget=${self.budget}, tier={self.loyalty_tier})"


class Booking:
    """Represents a confirmed reservation linking a client, package, and agent."""

    def __init__(self, booking_id, client, package, agent, status="pending"):
        self.booking_id = booking_id
        self.client = client
        self.package = package
        self.agent = agent
        self.status = status

    def __repr__(self):
        return f"Booking({self.booking_id}: {self.client.name} -> {self.package.name}, {self.status})"


class Agent:
    """Represents a travel agency employee."""

    def __init__(self, agent_id, name, specialization):
        self.agent_id = agent_id
        self.name = name
        self.specialization = specialization

    def __repr__(self):
        return f"Agent({self.name}, specializes in {self.specialization})"


# ---------------------------------------------------------------
# SECTION 2: KNOWLEDGE BASE
# ---------------------------------------------------------------

class TravelAgencyKB:
    """
    The central Knowledge Base.
    Stores all known facts: destinations, packages, clients, agents, bookings.
    """

    def __init__(self):
        self.destinations = []
        self.packages = []
        self.clients = []
        self.agents = []
        self.bookings = []
        self._booking_counter = 1

    def add_destination(self, dest):
        self.destinations.append(dest)

    def add_package(self, pkg):
        self.packages.append(pkg)

    def add_client(self, client):
        self.clients.append(client)

    def add_agent(self, agent):
        self.agents.append(agent)

    def register_booking(self, client, package, agent):
        """Creates and stores a new confirmed booking."""
        booking = Booking(
            booking_id=f"BK{self._booking_counter:04d}",
            client=client,
            package=package,
            agent=agent,
            status="confirmed"
        )
        self._booking_counter += 1
        client.booking_history.append(booking)
        self.bookings.append(booking)
        return booking


# ---------------------------------------------------------------
# SECTION 3: SAMPLE DATA (Seeding the Knowledge Base)
# ---------------------------------------------------------------

def build_sample_kb():
    """
    Populates the Knowledge Base with sample facts:
    destinations, packages, agents, and clients.
    """
    kb = TravelAgencyKB()

    # --- Destinations ---
    dubai = Destination(
        "Dubai", "UAE", "hot", visa_required=False,
        avg_cost_per_day=300,
        tags=["business hub", "luxury", "fast wifi", "conferences"]
    )
    singapore = Destination(
        "Singapore", "Singapore", "tropical", visa_required=False,
        avg_cost_per_day=250,
        tags=["business hub", "tech", "fast wifi", "safe"]
    )
    paris = Destination(
        "Paris", "France", "temperate", visa_required=True,
        avg_cost_per_day=200,
        tags=["leisure", "culture", "romance"]
    )
    nairobi = Destination(
        "Nairobi", "Kenya", "mild", visa_required=True,
        avg_cost_per_day=80,
        tags=["budget", "adventure", "nature"]
    )

    for d in [dubai, singapore, paris, nairobi]:
        kb.add_destination(d)

    # --- Travel Packages ---
    pkgs = [
        TravelPackage(
            "P001", "Dubai Executive", dubai, price=2500, duration_days=5,
            services=["business class flight", "5-star hotel", "airport transfer", "wifi lounge"],
            travel_class="business"
        ),
        TravelPackage(
            "P002", "Singapore Tech Summit", singapore, price=1800, duration_days=4,
            services=["economy flight", "4-star hotel", "conference access", "fast wifi"],
            travel_class="economy"
        ),
        TravelPackage(
            "P003", "Paris Getaway", paris, price=1500, duration_days=6,
            services=["economy flight", "3-star hotel", "city tour"],
            travel_class="economy"
        ),
        TravelPackage(
            "P004", "Nairobi Budget Explorer", nairobi, price=600, duration_days=7,
            services=["economy flight", "guesthouse", "safari day trip"],
            travel_class="economy"
        ),
        TravelPackage(
            "P005", "Dubai Luxury Plus", dubai, price=5000, duration_days=7,
            services=["first class flight", "7-star hotel", "personal concierge", "spa"],
            travel_class="first"
        ),
    ]
    for p in pkgs:
        kb.add_package(p)

    # --- Agents ---
    agents = [
        Agent("A001", "Sarah", "business travel"),
        Agent("A002", "James", "luxury travel"),
        Agent("A003", "Amina", "budget travel"),
    ]
    for a in agents:
        kb.add_agent(a)

    # --- Clients (Business Travelers) ---
    clients = [
        Client(
            "C001", "Alex Johnson", age=35, budget=3000,
            travel_type="business",
            preferences=["wifi", "business class", "short trips"],
            loyalty_tier="gold"
        ),
        Client(
            "C002", "Maria Gomez", age=28, budget=700,
            travel_type="business",
            preferences=["budget", "economy", "conferences"],
            loyalty_tier="standard"
        ),
        Client(
            "C003", "David Chen", age=45, budget=6000,
            travel_type="business",
            preferences=["luxury", "first class", "spa", "concierge"],
            loyalty_tier="platinum"
        ),
    ]
    for c in clients:
        kb.add_client(c)

    return kb


# ---------------------------------------------------------------
# SECTION 4: RULE ENGINE
# ---------------------------------------------------------------

LOYALTY_DISCOUNTS = {
    "standard":  0.00,
    "silver":    0.05,
    "gold":      0.10,
    "platinum":  0.15,
}


class RuleEngine:
    """
    Applies business rules to match clients with suitable travel packages.

    Rules implemented:
        Rule 1 - Budget Filter        : exclude packages above client budget
        Rule 2 - Preference Matching  : score packages by preference overlap
        Rule 3 - Loyalty Discount     : reduce price based on loyalty tier
        Rule 4 - Travel Class Match   : filter by preferred travel class
        Rule 5 - Agent Assignment     : assign the right agent to the client

    Bug fixes applied:
        - Agent assignment now checks budget before loyalty/preferences
        - Preference relaxation added so the system never hits a dead end
        - Budget boundary of exactly 1000 correctly routes to business agent
    """

    def __init__(self, kb):
        self.kb = kb

    # --- Rule 3: Loyalty Discount ---
    def apply_loyalty_discount(self, client, package):
        """
        IF client has a loyalty tier above standard
        THEN reduce the effective package price by the discount rate.
        """
        discount_rate = LOYALTY_DISCOUNTS.get(client.loyalty_tier, 0.0)
        discounted_price = package.price * (1 - discount_rate)
        return round(discounted_price, 2)

    # --- Rule 1: Budget Filter ---
    def passes_budget_filter(self, client, package):
        """
        IF effective price exceeds client budget THEN reject the package.
        """
        effective_price = self.apply_loyalty_discount(client, package)
        return effective_price <= client.budget

    # --- Rule 4: Travel Class Match ---
    def passes_class_filter(self, client, package):
        """
        IF client prefers business or first class
        THEN only allow packages that match those classes.
        If no class preference is stated, all classes are accepted.
        """
        class_preferences = []
        if "business class" in client.preferences:
            class_preferences.append("business")
        if "first class" in client.preferences:
            class_preferences.append("first")

        if not class_preferences:
            return True

        return package.travel_class in class_preferences

    # --- Rule 2: Preference Matching ---
    def compute_preference_score(self, client, package):
        """
        Counts how many of the client's preferences appear in
        the package services or destination tags.
        Higher score means better match.
        """
        score = 0
        searchable = package.services + package.destination.tags

        for preference in client.preferences:
            for item in searchable:
                if preference.lower() in item.lower():
                    score += 1
                    break

        return score

    # --- Rule 5: Agent Assignment ---
    def assign_agent(self, client):
        """
        Priority order (budget is always checked first):
        1. Budget strictly under 1000   -> budget travel agent (Amina)
        2. Platinum tier or luxury pref -> luxury travel agent (James)
        3. Everything else              -> business travel agent (Sarah)

        Note: A client with budget exactly at 1000 is treated as
        a standard business client, not a budget client.
        """
        agents = self.kb.agents

        if client.budget < 1000:
            specialization = "budget travel"
        elif client.loyalty_tier == "platinum" or "luxury" in client.preferences:
            specialization = "luxury travel"
        else:
            specialization = "business travel"

        for agent in agents:
            if agent.specialization == specialization:
                return agent

        return agents[0] if agents else None

    # --- Internal filtering and scoring ---
    def _filter_and_score(self, client, strict=True):
        """
        Filters packages by budget and optionally by travel class,
        then scores each surviving package by preference match.

        strict=True  applies the class filter (exact preference match)
        strict=False skips the class filter (budget only)
        """
        results = []

        for package in self.kb.packages:

            if not self.passes_budget_filter(client, package):
                continue

            if strict and not self.passes_class_filter(client, package):
                continue

            score = self.compute_preference_score(client, package)
            effective_price = self.apply_loyalty_discount(client, package)

            results.append({
                "package":         package,
                "score":           score,
                "original_price":  package.price,
                "effective_price": effective_price,
                "savings":         round(package.price - effective_price, 2),
                "relaxed":         not strict,
            })

        return results

    # --- Main Recommendation Method ---
    def recommend(self, client, top_n=3):
        """
        Runs all rules for a given client and returns top N packages.

        If strict filtering returns nothing, the system automatically
        relaxes the class filter and tries again before giving up.
        This prevents the system from ever hitting a silent dead end.
        """
        results = self._filter_and_score(client, strict=True)

        if not results:
            print("\n  No exact matches found. Searching for closest alternatives...")
            results = self._filter_and_score(client, strict=False)

        results.sort(key=lambda x: (-x["score"], x["effective_price"]))
        return results[:top_n]


# ---------------------------------------------------------------
# SECTION 5: DISPLAY FUNCTIONS
# ---------------------------------------------------------------

def print_kb_summary(kb):
    """Prints a readable summary of everything stored in the Knowledge Base."""
    print("\n" + "-" * 55)
    print("   TRAVEL AGENCY - KNOWLEDGE BASE SUMMARY")
    print("-" * 55)

    print(f"\nDESTINATIONS ({len(kb.destinations)})")
    for d in kb.destinations:
        print(f"  - {d.name}, {d.country} | ${d.avg_cost_per_day}/day | Tags: {', '.join(d.tags)}")

    print(f"\nTRAVEL PACKAGES ({len(kb.packages)})")
    for p in kb.packages:
        print(f"  - [{p.package_id}] {p.name} | ${p.price} | {p.duration_days} days | Class: {p.travel_class}")

    print(f"\nCLIENTS ({len(kb.clients)})")
    for c in kb.clients:
        print(f"  - [{c.client_id}] {c.name} | Budget: ${c.budget} | Tier: {c.loyalty_tier} | Prefs: {', '.join(c.preferences)}")

    print(f"\nAGENTS ({len(kb.agents)})")
    for a in kb.agents:
        print(f"  - [{a.agent_id}] {a.name} | Specialization: {a.specialization}")

    print(f"\nBOOKINGS ({len(kb.bookings)})")
    if kb.bookings:
        for b in kb.bookings:
            print(f"  - {b.booking_id} | {b.client.name} | {b.package.name} | {b.status.upper()}")
    else:
        print("  No bookings recorded yet.")

    print("\n" + "-" * 55 + "\n")


def print_recommendations(client, recommendations, agent):
    """Prints the rule engine recommendations for a given client."""
    print("\n" + "-" * 55)
    print(f"  RECOMMENDATIONS FOR: {client.name}")
    print(f"  Budget: ${client.budget} | Tier: {client.loyalty_tier}")
    print(f"  Preferences: {', '.join(client.preferences)}")
    print(f"  Assigned Agent: {agent.name} ({agent.specialization})")
    print("-" * 55)

    if not recommendations:
        print("  No suitable packages found for this client.")
    else:
        for rank, result in enumerate(recommendations, start=1):
            pkg = result["package"]
            print(f"\n  Rank {rank}: {pkg.name}")
            print(f"    Destination    : {pkg.destination.name}, {pkg.destination.country}")
            print(f"    Duration       : {pkg.duration_days} days")
            print(f"    Travel Class   : {pkg.travel_class}")
            print(f"    Original Price : ${result['original_price']}")
            print(f"    Your Price     : ${result['effective_price']}  (saving ${result['savings']})")
            print(f"    Match Score    : {result['score']} preference(s) matched")
            print(f"    Services       : {', '.join(pkg.services)}")
            if result.get("relaxed"):
                print(f"    Note           : Alternative suggestion outside your class preference")

    print("\n" + "-" * 55 + "\n")


# ---------------------------------------------------------------
# SECTION 6: CLIENT INTERACTION MODEL
# ---------------------------------------------------------------

VALID_PREFERENCES = [
    "wifi", "business class", "first class", "economy",
    "luxury", "budget", "spa", "concierge",
    "short trips", "conferences", "adventure", "nature"
]

VALID_TIERS = ["standard", "silver", "gold", "platinum"]


def collect_client_details(kb):
    """
    Interactively collects a new client's information from the terminal.
    Validates every input before accepting it.
    """
    print("\n" + "-" * 55)
    print("  WELCOME TO THE TRAVEL AGENCY BOOKING SYSTEM")
    print("  Please answer the following questions.")
    print("-" * 55)

    # --- Name ---
    while True:
        name = input("\nEnter your full name: ").strip()
        if name:
            break
        print("  Name cannot be empty. Please try again.")

    # --- Age ---
    while True:
        age_input = input("Enter your age: ").strip()
        if age_input.isdigit() and 18 <= int(age_input) <= 100:
            age = int(age_input)
            break
        print("  Please enter a valid age between 18 and 100.")

    # --- Budget ---
    while True:
        budget_input = input("Enter your maximum travel budget in USD: $").strip()
        if budget_input.isdigit() and int(budget_input) > 0:
            budget = int(budget_input)
            break
        print("  Please enter a valid budget (whole number greater than 0).")

    # --- Loyalty Tier ---
    print(f"\nLoyalty tiers available: {', '.join(VALID_TIERS)}")
    while True:
        tier = input("Enter your loyalty tier (or press Enter for 'standard'): ").strip().lower()
        if tier == "":
            tier = "standard"
        if tier in VALID_TIERS:
            break
        print(f"  Invalid tier. Choose from: {', '.join(VALID_TIERS)}")

    # --- Preferences ---
    print(f"\nAvailable preferences:")
    for i, pref in enumerate(VALID_PREFERENCES, start=1):
        print(f"  {i}. {pref}")

    while True:
        raw = input(
            "\nEnter your preferences as numbers separated by commas (e.g. 1,3,5): "
        ).strip()
        try:
            indices = [int(x.strip()) for x in raw.split(",")]
            if all(1 <= i <= len(VALID_PREFERENCES) for i in indices):
                preferences = [VALID_PREFERENCES[i - 1] for i in indices]
                break
            else:
                print(f"  Please enter numbers between 1 and {len(VALID_PREFERENCES)}.")
        except ValueError:
            print("  Invalid input. Use numbers separated by commas, e.g. 1,3,5")

    new_id = f"C{len(kb.clients) + 1:03d}"

    client = Client(
        client_id=new_id,
        name=name,
        age=age,
        budget=budget,
        travel_type="business",
        preferences=preferences,
        loyalty_tier=tier
    )

    print(f"\n  Client profile created for: {name}")
    return client


def display_package_menu(recommendations):
    """
    Displays recommended packages as a numbered menu.
    Clearly labels relaxed results as alternative suggestions.
    """
    if not recommendations:
        print("\n" + "-" * 55)
        print("  NO PACKAGES AVAILABLE")
        print("-" * 55)
        print("  Unfortunately no packages are available within")
        print("  your budget at this time.")
        print("  Please speak to your assigned agent for custom options.")
        print("-" * 55)
        return []

    is_relaxed = any(r.get("relaxed", False) for r in recommendations)

    print("\n" + "-" * 55)
    if is_relaxed:
        print("  CLOSEST AVAILABLE PACKAGES")
        print("  (No exact matches found - showing best alternatives)")
    else:
        print("  YOUR RECOMMENDED PACKAGES")
    print("-" * 55)

    for i, result in enumerate(recommendations, start=1):
        pkg = result["package"]
        print(f"\n  Option {i}: {pkg.name}")
        print(f"    Destination    : {pkg.destination.name}, {pkg.destination.country}")
        print(f"    Duration       : {pkg.duration_days} days")
        print(f"    Travel Class   : {pkg.travel_class}")
        print(f"    Original Price : ${result['original_price']}")
        print(f"    Your Price     : ${result['effective_price']}  (saving ${result['savings']})")
        print(f"    Match Score    : {result['score']} preference(s) matched")
        print(f"    Services       : {', '.join(pkg.services)}")
        if result.get("relaxed"):
            print(f"    Note           : Alternative suggestion outside your class preference")

    return recommendations


def select_package(recommendations):
    """
    Asks the client to choose one of the recommended packages.
    Returns the chosen result or None if they cancel.
    """
    if not recommendations:
        return None

    while True:
        choice = input(
            f"\nEnter the option number you want to book (1-{len(recommendations)})"
            f" or type 'exit' to cancel: "
        ).strip().lower()

        if choice == "exit":
            print("\n  Booking cancelled. Thank you for visiting.")
            return None

        if choice.isdigit() and 1 <= int(choice) <= len(recommendations):
            return recommendations[int(choice) - 1]

        print(f"  Please enter a number between 1 and {len(recommendations)}, or 'exit'.")


def confirm_booking(kb, client, selected_result, agent):
    """
    Confirms the booking, saves it to the Knowledge Base,
    and prints a booking confirmation summary.
    """
    package = selected_result["package"]

    if client not in kb.clients:
        kb.add_client(client)

    booking = kb.register_booking(client, package, agent)

    print("\n" + "-" * 55)
    print("  BOOKING CONFIRMED")
    print("-" * 55)
    print(f"  Booking ID     : {booking.booking_id}")
    print(f"  Client         : {client.name}")
    print(f"  Package        : {package.name}")
    print(f"  Destination    : {package.destination.name}, {package.destination.country}")
    print(f"  Duration       : {package.duration_days} days")
    print(f"  Travel Class   : {package.travel_class}")
    print(f"  Amount Charged : ${selected_result['effective_price']}")
    print(f"  You Saved      : ${selected_result['savings']}")
    print(f"  Your Agent     : {agent.name} ({agent.specialization})")
    print(f"  Status         : {booking.status.upper()}")
    print("-" * 55)
    print(f"\n  Thank you, {client.name}. {agent.name} will be in touch shortly.")
    print("-" * 55 + "\n")

    return booking


# ---------------------------------------------------------------
# SECTION 7: SEARCH, REPORTS AND STATISTICS
# ---------------------------------------------------------------

def search_client_by_name(kb, search_term):
    """
    Searches the knowledge base for clients whose name contains
    the search term (case insensitive).
    Returns a list of matching clients.
    """
    search_term = search_term.lower().strip()
    matches = [c for c in kb.clients if search_term in c.name.lower()]
    return matches


def display_client_profile(client):
    """
    Prints a full profile for a single client including
    their details and complete booking history.
    """
    print("\n" + "-" * 55)
    print(f"  CLIENT PROFILE: {client.name}")
    print("-" * 55)
    print(f"  ID             : {client.client_id}")
    print(f"  Age            : {client.age}")
    print(f"  Budget         : ${client.budget}")
    print(f"  Loyalty Tier   : {client.loyalty_tier}")
    print(f"  Travel Type    : {client.travel_type}")
    print(f"  Preferences    : {', '.join(client.preferences)}")
    print(f"\n  Booking History ({len(client.booking_history)} bookings)")

    if not client.booking_history:
        print("  No bookings on record.")
    else:
        for b in client.booking_history:
            print(f"    - [{b.booking_id}] {b.package.name} "
                  f"| ${b.package.price} | {b.status.upper()}")
    print("-" * 55)


def cancel_booking(kb, booking_id):
    """
    Finds a booking by its ID and sets its status to cancelled.
    Returns the booking if found, None otherwise.
    """
    for booking in kb.bookings:
        if booking.booking_id == booking_id.upper().strip():
            if booking.status == "cancelled":
                print(f"\n  Booking {booking_id} is already cancelled.")
                return booking
            booking.status = "cancelled"
            print(f"\n  Booking {booking_id} has been successfully cancelled.")
            print(f"  Client  : {booking.client.name}")
            print(f"  Package : {booking.package.name}")
            return booking

    print(f"\n  No booking found with ID: {booking_id}")
    return None


def generate_statistics(kb):
    """
    Calculates and displays a summary dashboard of system activity.
    Covers bookings, revenue, popular destinations, and agent workload.
    """
    print("\n" + "-" * 55)
    print("  AGENCY STATISTICS DASHBOARD")
    print("-" * 55)

    confirmed = [b for b in kb.bookings if b.status == "confirmed"]
    cancelled = [b for b in kb.bookings if b.status == "cancelled"]

    print(f"\n  Total Bookings     : {len(kb.bookings)}")
    print(f"  Confirmed          : {len(confirmed)}")
    print(f"  Cancelled          : {len(cancelled)}")
    print(f"  Total Clients      : {len(kb.clients)}")
    print(f"  Total Packages     : {len(kb.packages)}")

    revenue = sum(b.package.price for b in confirmed)
    print(f"\n  Total Revenue      : ${revenue:,.2f}  (confirmed bookings only)")

    if confirmed:
        destination_counts = {}
        for b in confirmed:
            dest = b.package.destination.name
            destination_counts[dest] = destination_counts.get(dest, 0) + 1
        top_dest = max(destination_counts, key=destination_counts.get)
        print(f"  Top Destination    : {top_dest} ({destination_counts[top_dest]} booking(s))")

        agent_counts = {}
        for b in confirmed:
            agent_name = b.agent.name
            agent_counts[agent_name] = agent_counts.get(agent_name, 0) + 1
        top_agent = max(agent_counts, key=agent_counts.get)
        print(f"  Busiest Agent      : {top_agent} ({agent_counts[top_agent]} booking(s))")

        avg_value = revenue / len(confirmed)
        print(f"  Avg Booking Value  : ${avg_value:,.2f}")
    else:
        print("\n  No confirmed bookings yet to calculate statistics.")

    print("\n" + "-" * 55 + "\n")


def export_booking_report(kb, filename="booking_report.txt"):
    """
    Exports all booking data to a plain text file.
    Creates the file in the same directory as the script.
    """
    lines = []
    lines.append("=" * 55)
    lines.append("   TRAVEL AGENCY - BOOKING REPORT")
    lines.append("=" * 55)
    lines.append(f"   Total Bookings : {len(kb.bookings)}")
    lines.append(f"   Total Clients  : {len(kb.clients)}")
    lines.append("")

    if not kb.bookings:
        lines.append("   No bookings recorded.")
    else:
        for b in kb.bookings:
            lines.append("-" * 55)
            lines.append(f"  Booking ID     : {b.booking_id}")
            lines.append(f"  Status         : {b.status.upper()}")
            lines.append(f"  Client         : {b.client.name} (Tier: {b.client.loyalty_tier})")
            lines.append(f"  Package        : {b.package.name}")
            lines.append(f"  Destination    : {b.package.destination.name}, {b.package.destination.country}")
            lines.append(f"  Duration       : {b.package.duration_days} days")
            lines.append(f"  Travel Class   : {b.package.travel_class}")
            lines.append(f"  Package Price  : ${b.package.price}")
            lines.append(f"  Agent          : {b.agent.name} ({b.agent.specialization})")
            lines.append("")

    lines.append("=" * 55)
    lines.append("   END OF REPORT")
    lines.append("=" * 55)

    with open(filename, "w") as f:
        f.write("\n".join(lines))

    print(f"\n  Report successfully exported to: {filename}")
    print(f"  Total bookings recorded: {len(kb.bookings)}")


# ---------------------------------------------------------------
# SECTION 8: MAIN INTERACTIVE SESSION
# ---------------------------------------------------------------

def run_interactive_session(kb):
    """
    Runs the full interactive travel agency system.
    Menu options:
        1. New client booking
        2. View all bookings
        3. Search client by name
        4. Cancel a booking
        5. View statistics dashboard
        6. Export booking report
        7. View knowledge base summary
        8. Exit
    """
    engine = RuleEngine(kb)

    while True:
        print("\n" + "=" * 55)
        print("  TRAVEL AGENCY - CLIENT SERVICES DESK")
        print("=" * 55)
        print("  1. New client booking")
        print("  2. View all bookings")
        print("  3. Search client by name")
        print("  4. Cancel a booking")
        print("  5. View statistics dashboard")
        print("  6. Export booking report")
        print("  7. View knowledge base summary")
        print("  8. Exit")
        print("-" * 55)

        choice = input("  Select an option (1-8): ").strip()

        if choice == "1":
            client = collect_client_details(kb)
            recommendations = engine.recommend(client, top_n=3)
            agent = engine.assign_agent(client)

            print(f"\n  Assigned Agent: {agent.name} ({agent.specialization})")

            recommendations = display_package_menu(recommendations)

            if not recommendations:
                continue

            selected = select_package(recommendations)

            if selected is None:
                continue

            confirm_booking(kb, client, selected, agent)

        elif choice == "2":
            print("\n" + "-" * 55)
            print(f"  ALL BOOKINGS ({len(kb.bookings)})")
            print("-" * 55)
            if not kb.bookings:
                print("  No bookings recorded yet.")
            for b in kb.bookings:
                print(f"  - {b.booking_id} | {b.client.name} | "
                      f"{b.package.name} | {b.status.upper()}")
            print("-" * 55)

        elif choice == "3":
            term = input("\n  Enter client name to search: ").strip()
            matches = search_client_by_name(kb, term)
            if not matches:
                print(f"\n  No clients found matching: {term}")
            else:
                print(f"\n  Found {len(matches)} client(s):")
                for client in matches:
                    display_client_profile(client)

        elif choice == "4":
            booking_id = input("\n  Enter booking ID to cancel (e.g. BK0001): ").strip()
            cancel_booking(kb, booking_id)

        elif choice == "5":
            generate_statistics(kb)

        elif choice == "6":
            filename = input(
                "\n  Enter filename for report (press Enter for 'booking_report.txt'): "
            ).strip()
            if not filename:
                filename = "booking_report.txt"
            if not filename.endswith(".txt"):
                filename += ".txt"
            export_booking_report(kb, filename)

        elif choice == "7":
            print_kb_summary(kb)

        elif choice == "8":
            print("\n  Thank you for using the Travel Agency System. Goodbye.\n")
            break

        else:
            print("  Invalid option. Please enter a number between 1 and 8.")


# ---------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------

if __name__ == "__main__":
    kb = build_sample_kb()
    run_interactive_session(kb)