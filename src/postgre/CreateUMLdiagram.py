from graphviz import Digraph

# Création du diagramme UML
dot_specific = Digraph()
dot_specific.attr(rankdir="TB", size="10", splines="false")

# Tables avec la configuration des champs
tables_specific = {
    "Bank": [
        ("businessUnitId", "int", "PK"),
        ("identifyingName", "str", ""),
        ("displayName", "str", ""),
        ("logoUrl", "str", ""),
        ("numberOfReviews", "int", ""),
        ("trustScore", "float", ""),
        ("isRecommendedInCategories", "bool", ""),
    ],
    "Location": [
        ("locationId", "int", "PK"),
        ("address", "str", ""),
        ("city", "str", ""),
        ("zipCode", "str", ""),
        ("country", "str", ""),
        ("businessUnitId", "int", "FK"),
    ],
    "Contact": [
        ("contactId", "int", "PK"),
        ("website", "str", ""),
        ("email", "str", ""),
        ("phone", "str", ""),
        ("businessUnitId", "int", "FK"),
    ],
    "Category": [
        ("categoryId", "int", "PK"),
        ("displayName", "str", ""),
        ("isPredicted", "bool", ""),
    ],
    "BankCategory": [("businessUnitId", "int", "FK"), ("categoryId", "int", "FK")],
}

# Ajout des tables au diagramme
for table, fields in tables_specific.items():
    field_str = "".join(
        (
            f'<TR><TD ALIGN="LEFT"><B><U>{field}: {ftype}</U></B></TD></TR>'
            if "PK" in flags
            else (
                f'<TR><TD ALIGN="LEFT"><B>{field}: {ftype}</B></TD></TR>'
                if "FK" in flags
                else f'<TR><TD ALIGN="LEFT">{field}: {ftype}</TD></TR>'
            )
        )
        for field, ftype, flags in fields
    )

    dot_specific.node(
        table,
        f"""<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
            <TR><TD BORDER="1"><B>{table}</B></TD></TR>
            <TR><TD BORDER="1">
                <TABLE BORDER="0" CELLSPACING="0">
                    {field_str}
                </TABLE>
            </TD></TR>
        </TABLE>>""",
        shape="plaintext",
    )

# Reproduction des relations
relations_specific = [
    ("Bank", "Location", "1", "1", "sw", "ne"),
    ("Bank", "Contact", "1", "1", "se", "nw"),
    ("Bank", "BankCategory", "1", "*", "s", "n"),
    ("BankCategory", "Category", "*", "1", "s", "n"),
]

# Ajout des relations
for src, dst, src_card, dst_card, src_port, dst_port in relations_specific:
    dot_specific.edge(
        src,
        dst,
        tailport=src_port,
        headport=dst_port,
        headlabel=f"{dst_card}..{src_card}",
        taillabel="",
        arrowhead="none",
        arrowtail="none",
    )

# Rendu final du diagramme
dot_specific.render("data/Bank_UML_Diagram", format="png", cleanup=True)
dot_specific
