import streamlit as st
import pandas as pd
import re

# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="DataLens AI",
    page_icon="◈",
    layout="wide"
)


# --------------------------------------------------
# DATALENS AI — FUTURISTIC UI
# --------------------------------------------------

st.html("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');


/* ==================================================
   GLOBAL BACKGROUND
   ================================================== */

.stApp {
    background:
        radial-gradient(circle at 10% 15%, rgba(0, 229, 255, 0.10), transparent 25%),
        radial-gradient(circle at 90% 20%, rgba(168, 85, 247, 0.14), transparent 28%),
        radial-gradient(circle at 50% 100%, rgba(236, 72, 153, 0.08), transparent 30%),
        #050711 !important;
}


/* animated cyber grid */

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;

    background-image:
        linear-gradient(rgba(0,229,255,0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,229,255,0.035) 1px, transparent 1px);

    background-size: 55px 55px;

    mask-image: linear-gradient(
        to bottom,
        black 0%,
        rgba(0,0,0,0.75) 45%,
        transparent 100%
    );

    animation: gridMove 18s linear infinite;
}

@keyframes gridMove {
    from {
        transform: translateY(0);
    }

    to {
        transform: translateY(55px);
    }
}


/* ==================================================
   FLOATING BACKGROUND GLOWS
   ================================================== */

.stApp::after {
    content: "";
    position: fixed;
    width: 420px;
    height: 420px;
    border-radius: 50%;

    right: -160px;
    top: 180px;

    background:
        radial-gradient(
            circle,
            rgba(124,58,237,0.22),
            rgba(0,229,255,0.06),
            transparent 70%
        );

    filter: blur(12px);
    pointer-events: none;

    animation: backgroundFloat 7s ease-in-out infinite;
}

@keyframes backgroundFloat {

    0%,100% {
        transform: translate(0,0);
    }

    50% {
        transform: translate(-35px,35px);
    }
}


/* ==================================================
   HERO FRAME
   ================================================== */

.dl-hero {

    position: relative;

    min-height: 500px;

    padding: 52px 55px;

    margin-top: 15px;
    margin-bottom: 30px;

    overflow: hidden;

    border-radius: 32px;

    background:
        linear-gradient(
            135deg,
            rgba(10,15,30,0.97),
            rgba(11,8,28,0.95)
        );

    border: 1px solid transparent;

    background-clip: padding-box;

    box-shadow:
        0 0 0 1px rgba(0,229,255,0.10),
        0 0 55px rgba(124,58,237,0.15),
        inset 0 0 50px rgba(0,229,255,0.025);
}


/* glowing border */

.dl-hero::before {

    content: "";

    position: absolute;

    inset: -2px;

    border-radius: 34px;

    background:
        linear-gradient(
            110deg,
            rgba(0,229,255,0.85),
            rgba(124,58,237,0.75),
            rgba(236,72,153,0.75),
            rgba(0,229,255,0.85)
        );

    z-index: -1;

    background-size: 300% 300%;

    animation: borderFlow 8s ease infinite;
}

@keyframes borderFlow {

    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }
}


/* ==================================================
   DECORATIVE DATA PARTICLES
   ================================================== */

.particle {

    position: absolute;

    width: 5px;
    height: 5px;

    border-radius: 50%;

    background: #00e5ff;

    box-shadow:
        0 0 12px #00e5ff,
        0 0 25px rgba(0,229,255,0.6);

    animation: particleFloat 5s ease-in-out infinite;
}

.p1 {
    left: 8%;
    top: 18%;
}

.p2 {
    left: 45%;
    top: 12%;
    animation-delay: 1s;
}

.p3 {
    left: 68%;
    top: 72%;
    animation-delay: 2s;
}

.p4 {
    left: 88%;
    top: 45%;
    animation-delay: 3s;
}

.p5 {
    left: 30%;
    top: 86%;
    animation-delay: 1.5s;
}

@keyframes particleFloat {

    0%,100% {
        transform: translateY(0);
        opacity: 0.4;
    }

    50% {
        transform: translateY(-18px);
        opacity: 1;
    }
}


/* ==================================================
   HERO CONTENT
   ================================================== */

.dl-content {

    position: relative;

    z-index: 5;

    max-width: 700px;
}


.dl-status {

    display: inline-flex;

    align-items: center;
    gap: 9px;

    padding: 8px 15px;

    border-radius: 30px;

    background: rgba(0,229,255,0.07);

    border: 1px solid rgba(0,229,255,0.28);

    color: #67e8f9;

    font-size: 12px;

    font-weight: 700;

    letter-spacing: 1.3px;

    box-shadow:
        0 0 20px rgba(0,229,255,0.08);
}


.status-dot {

    width: 8px;
    height: 8px;

    border-radius: 50%;

    background: #22d3ee;

    box-shadow:
        0 0 8px #22d3ee,
        0 0 16px #22d3ee;

    animation: statusPulse 1.6s ease-in-out infinite;
}

@keyframes statusPulse {

    0%,100% {
        opacity: 0.45;
        transform: scale(0.85);
    }

    50% {
        opacity: 1;
        transform: scale(1.15);
    }
}


/* main title */

.dl-title {

    margin-top: 26px;

    font-family: Inter, sans-serif;

    font-size: 58px;

    line-height: 1.02;

    font-weight: 800;

    letter-spacing: -2.5px;

    color: #f8fafc;
}


.dl-title .gradient {

    background:
        linear-gradient(
            90deg,
            #22d3ee,
            #8b5cf6,
            #ec4899
        );

    background-size: 200% auto;

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;

    animation: textGradient 5s linear infinite;
}

@keyframes textGradient {

    0% {
        background-position: 0% center;
    }

    100% {
        background-position: 200% center;
    }
}


.dl-description {

    margin-top: 22px;

    max-width: 650px;

    color: #aab5ca;

    font-size: 17px;

    line-height: 1.7;
}


/* ==================================================
   FEATURE PILLS
   ================================================== */

.dl-pills {

    display: flex;

    gap: 10px;

    flex-wrap: wrap;

    margin-top: 28px;
}


.dl-pill {

    padding: 9px 14px;

    border-radius: 12px;

    color: #dbeafe;

    background: rgba(255,255,255,0.035);

    border: 1px solid rgba(255,255,255,0.09);

    font-size: 13px;

    backdrop-filter: blur(12px);

    transition: 0.25s;
}

.dl-pill:hover {

    border-color: rgba(0,229,255,0.5);

    box-shadow:
        0 0 20px rgba(0,229,255,0.12);

    transform: translateY(-2px);
}


/* ==================================================
   AI VISUALIZATION
   ================================================== */

.ai-visual {

    position: absolute;

    right: 55px;
    top: 80px;

    width: 320px;
    height: 320px;
}


/* orbit rings */

.orbit {

    position: absolute;

    inset: 20px;

    border-radius: 50%;

    border: 1px solid rgba(0,229,255,0.18);

    animation: orbitRotate 12s linear infinite;
}

.orbit.two {

    inset: 48px;

    border-color: rgba(139,92,246,0.22);

    animation-duration: 8s;

    animation-direction: reverse;
}

.orbit.three {

    inset: 78px;

    border-color: rgba(236,72,153,0.18);

    animation-duration: 6s;
}


@keyframes orbitRotate {

    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}


/* center AI core */

.ai-core {

    position: absolute;

    left: 50%;
    top: 50%;

    transform: translate(-50%, -50%);

    width: 115px;
    height: 115px;

    border-radius: 32px;

    display: flex;

    align-items: center;
    justify-content: center;

    background:
        linear-gradient(
            145deg,
            rgba(0,229,255,0.14),
            rgba(124,58,237,0.25)
        );

    border: 1px solid rgba(103,232,249,0.45);

    box-shadow:
        0 0 25px rgba(0,229,255,0.25),
        0 0 65px rgba(124,58,237,0.22),
        inset 0 0 25px rgba(255,255,255,0.04);

    animation: corePulse 3s ease-in-out infinite;
}

@keyframes corePulse {

    0%,100% {
        transform: translate(-50%,-50%) scale(1);
    }

    50% {
        transform: translate(-50%,-50%) scale(1.06);
    }
}


.ai-bars {

    display: flex;

    align-items: end;

    gap: 7px;

    height: 55px;
}


.ai-bar {

    width: 11px;

    border-radius: 6px 6px 2px 2px;

    background:
        linear-gradient(
            to top,
            #22d3ee,
            #8b5cf6,
            #ec4899
        );

    box-shadow:
        0 0 12px rgba(34,211,238,0.35);

    animation: barPulse 2s ease-in-out infinite;
}

.bar1 {
    height: 25px;
}

.bar2 {
    height: 42px;
    animation-delay: .25s;
}

.bar3 {
    height: 58px;
    animation-delay: .5s;
}

.bar4 {
    height: 35px;
    animation-delay: .75s;
}

@keyframes barPulse {

    0%,100% {
        transform: scaleY(0.75);
    }

    50% {
        transform: scaleY(1);
    }
}


/* orbit nodes */

.node {

    position: absolute;

    width: 10px;
    height: 10px;

    border-radius: 50%;

    background: #22d3ee;

    box-shadow:
        0 0 12px #22d3ee,
        0 0 25px rgba(34,211,238,0.7);
}

.node1 {
    top: 15px;
    left: 145px;
}

.node2 {
    right: 18px;
    top: 145px;
    background: #a78bfa;
    box-shadow: 0 0 15px #a78bfa;
}

.node3 {
    bottom: 20px;
    left: 145px;
    background: #f472b6;
    box-shadow: 0 0 15px #f472b6;
}


/* ==================================================
   SMALL DATA LABELS
   ================================================== */

.data-label {

    position: absolute;

    padding: 7px 11px;

    border-radius: 9px;

    font-size: 10px;

    color: #cbd5e1;

    background: rgba(8,11,20,0.7);

    border: 1px solid rgba(255,255,255,0.08);

    backdrop-filter: blur(12px);

    animation: labelFloat 4s ease-in-out infinite;
}

.label1 {
    top: 25px;
    right: 0;
}

.label2 {
    bottom: 42px;
    left: 0;
    animation-delay: 1s;
}

@keyframes labelFloat {

    0%,100% {
        transform: translateY(0);
    }

    50% {
        transform: translateY(-7px);
    }
}


/* ==================================================
   MOBILE
   ================================================== */

@media (max-width: 900px) {

    .ai-visual {
        opacity: 0.22;
        right: -80px;
    }

    .dl-title {
        font-size: 42px;
    }

    .dl-hero {
        padding: 38px 28px;
    }
}

</style>


<div class="dl-hero">

    <!-- animated particles -->

    <div class="particle p1"></div>
    <div class="particle p2"></div>
    <div class="particle p3"></div>
    <div class="particle p4"></div>
    <div class="particle p5"></div>


    <!-- main content -->

    <div class="dl-content">

        <div class="dl-status">
            <span class="status-dot"></span>
            DATALENS AI • LIVE ANALYTICS
        </div>


        <div class="dl-title">

            TALK TO YOUR DATA.<br>

            <span class="gradient">
                GET THE INSIGHT.
            </span>

        </div>


        <div class="dl-description">

            Upload any CSV or Excel dataset.
            Ask questions in plain English.
            DataLens automatically understands your schema,
            analyzes your data, and turns it into clear insights.

        </div>


        <div class="dl-pills">

            <div class="dl-pill">◈ Schema-Agnostic</div>

            <div class="dl-pill">⚡ Instant Analysis</div>

            <div class="dl-pill">✦ AI Powered</div>

            <div class="dl-pill">⌘ No SQL Required</div>

        </div>

    </div>


    <!-- AI DATA VISUAL -->

    <div class="ai-visual">

        <div class="orbit"></div>
        <div class="orbit two"></div>
        <div class="orbit three"></div>


        <div class="node node1"></div>
        <div class="node node2"></div>
        <div class="node node3"></div>


        <div class="ai-core">

            <div class="ai-bars">

                <div class="ai-bar bar1"></div>
                <div class="ai-bar bar2"></div>
                <div class="ai-bar bar3"></div>
                <div class="ai-bar bar4"></div>

            </div>

        </div>


        <div class="data-label label1">
            AI • ANALYZING
        </div>

        <div class="data-label label2">
            DATA → INSIGHT
        </div>

    </div>

</div>

""")
# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "📁 Upload your CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    # --------------------------------------------------
    # READ FILE
    # --------------------------------------------------

    try:
        if uploaded_file.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

    except Exception as e:
        st.error(f"❌ Could not read the file: {e}")
        st.stop()

    st.success("✅ File uploaded successfully!")

    # --------------------------------------------------
    # DATASET OVERVIEW
    # --------------------------------------------------

    rows, columns = df.shape

    st.subheader("📌 Dataset Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rows", rows)

    with col2:
        st.metric("Columns", columns)

    with col3:
        st.metric("Missing Values", int(df.isnull().sum().sum()))

    # --------------------------------------------------
    # DATA PREVIEW
    # --------------------------------------------------

    st.subheader("👀 Data Preview")

    st.dataframe(
        df.head(10),
        use_container_width=True
    )

    # --------------------------------------------------
    # AUTOMATIC SCHEMA DETECTION
    # --------------------------------------------------

    st.subheader("🔍 Detected Schema")

    schema = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Missing Values": df.isnull().sum().values
    })

    st.dataframe(
        schema,
        use_container_width=True
    )

    # --------------------------------------------------
    # IDENTIFY COLUMN TYPES
    # --------------------------------------------------

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    text_columns = df.select_dtypes(
        include=["object", "string", "category"]
    ).columns.tolist()

    # --------------------------------------------------
    # HELPER FUNCTIONS
    # --------------------------------------------------

    def normalize(text):
        """Convert text to a simple comparable form."""
        text = str(text).lower().strip()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text

    def find_numeric_column(question):
        """
        Find the numeric column referred to by the question.
        Works with exact names and common business terms.
        """

        q = normalize(question)

        # Exact column name match
        for column in numeric_columns:
            if normalize(column) in q:
                return column

        # Common semantic mappings
        aliases = {
            "sales": [
                "sales",
                "sale",
                "revenue",
                "income",
                "turnover",
                "earnings",
                "amount",
                "money",
                "value"
            ],
            "quantity": [
                "quantity",
                "qty",
                "units",
                "number sold",
                "items"
            ],
            "price": [
                "price",
                "cost",
                "rate"
            ]
        }

        for column in numeric_columns:
            column_name = normalize(column)

            for group in aliases.values():
                for word in group:
                    if word in q and (
                        word in column_name
                        or len(numeric_columns) == 1
                    ):
                        return column

        # If there is only one numeric column,
        # safely use it.
        if len(numeric_columns) == 1:
            return numeric_columns[0]

        return None

    def find_group_column(question):
        """
        Find a categorical column used for grouping.
        """

        q = normalize(question)

        # Exact column name
        for column in text_columns:
            if normalize(column) in q:
                return column

        # Natural language references
        for column in text_columns:

            column_name = normalize(column)

            if "product" in q and "product" in column_name:
                return column

            if "region" in q and "region" in column_name:
                return column

            if "category" in q and "category" in column_name:
                return column

            if "customer" in q and "customer" in column_name:
                return column

            if "country" in q and "country" in column_name:
                return column

            if "city" in q and "city" in column_name:
                return column

        return None

    def find_filter(df, question):
        """
        Find a categorical value mentioned in the question.
        Example:
        'sales of laptop'
        -> Product = Laptop
        """

        q = normalize(question)

        best_value = None
        best_column = None

        for column in text_columns:

            values = df[column].dropna().unique()

            for value in values:

                value_text = normalize(value)

                if len(value_text) < 2:
                    continue

                if value_text in q:
                    best_value = value
                    best_column = column

        return best_column, best_value

    def filter_dataframe(df, filter_column, filter_value):

        if filter_column is None or filter_value is None:
            return df

        return df[
            df[filter_column]
            .astype(str)
            .str.lower()
            .str.strip()
            == str(filter_value).lower().strip()
        ]

    # --------------------------------------------------
    # ASK YOUR DATA
    # --------------------------------------------------

    st.subheader("💬 Ask Your Data")

    question = st.text_input(
        "Ask a question about your dataset:",
        placeholder="Example: What is the total sales?"
    )

    if question:

        question_lower = normalize(question)

        # Find relevant columns
        numeric_column = find_numeric_column(question)

        filter_column, filter_value = find_filter(
            df,
            question
        )

        group_column = find_group_column(
            question
        )

        # --------------------------------------------------
        # APPLY FILTER
        # --------------------------------------------------

        working_df = filter_dataframe(
            df,
            filter_column,
            filter_value
        )

        # --------------------------------------------------
        # DETECT GROUP / COMPARISON QUESTIONS
        # --------------------------------------------------

        is_group_question = (
            " by " in f" {question_lower} "
            or "compare" in question_lower
            or "group" in question_lower
            or "which product" in question_lower
            or "which region" in question_lower
            or "which category" in question_lower
            or "show" in question_lower
        )

        # --------------------------------------------------
        # GROUP ANALYSIS
        # --------------------------------------------------

        if (
            is_group_question
            and group_column is not None
            and numeric_column is not None
            and filter_value is None
        ):

            grouped = (
                df.groupby(group_column)[numeric_column]
                .sum()
                .sort_values(ascending=False)
            )

            st.subheader(
                f"📊 {numeric_column} by {group_column}"
            )

            st.bar_chart(grouped)

            result_table = grouped.reset_index(
                name=f"Total {numeric_column}"
            )

            st.dataframe(
                result_table,
                use_container_width=True
            )

            highest_group = grouped.index[0]
            highest_value = grouped.iloc[0]

            st.success(
                f"🏆 {highest_group} has the highest total "
                f"{numeric_column}: {highest_value:,.2f}"
            )

            st.info(
                f"🧠 I grouped the data by {group_column}, "
                f"calculated the total {numeric_column} "
                f"for each group, and compared the results."
            )

        # --------------------------------------------------
        # TOTAL / SUM
        # --------------------------------------------------

        elif (
            numeric_column is not None
            and (
                "total" in question_lower
                or "sum" in question_lower
                or "overall" in question_lower
            )
        ):

            result = working_df[numeric_column].sum()

            if filter_value is not None:

                st.success(
                    f"💰 Total {numeric_column} for "
                    f"{filter_value}: {result:,.2f}"
                )

                st.info(
                    f"🧠 I filtered {filter_column} for "
                    f"'{filter_value}' and then calculated "
                    f"the total {numeric_column}."
                )

            else:

                st.success(
                    f"💰 Total {numeric_column}: "
                    f"{result:,.2f}"
                )

                st.info(
                    f"🧠 I calculated the sum of the "
                    f"{numeric_column} column."
                )

        # --------------------------------------------------
        # AVERAGE / MEAN
        # --------------------------------------------------

        elif (
            numeric_column is not None
            and (
                "average" in question_lower
                or "mean" in question_lower
                or "avg" in question_lower
            )
        ):

            result = working_df[numeric_column].mean()

            if filter_value is not None:

                st.success(
                    f"📊 Average {numeric_column} for "
                    f"{filter_value}: {result:,.2f}"
                )

                st.info(
                    f"🧠 I filtered {filter_column} for "
                    f"'{filter_value}' and calculated "
                    f"the average {numeric_column}."
                )

            else:

                st.success(
                    f"📊 Average {numeric_column}: "
                    f"{result:,.2f}"
                )

                st.info(
                    f"🧠 I calculated the mean of the "
                    f"{numeric_column} column."
                )

        # --------------------------------------------------
        # HIGHEST / MAXIMUM
        # --------------------------------------------------

        elif (
            numeric_column is not None
            and (
                "highest" in question_lower
                or "maximum" in question_lower
                or "max" in question_lower
                or "largest" in question_lower
            )
        ):

            result = working_df[numeric_column].max()

            st.success(
                f"🔝 Highest {numeric_column}: "
                f"{result:,.2f}"
            )

            # Find row containing maximum
            max_index = working_df[numeric_column].idxmax()

            max_row = working_df.loc[max_index]

            st.write("📌 Related record:")

            st.dataframe(
                pd.DataFrame([max_row]),
                use_container_width=True
            )

            st.info(
                f"🧠 I searched the {numeric_column} "
                f"column and identified the largest value."
            )

        # --------------------------------------------------
        # LOWEST / MINIMUM
        # --------------------------------------------------

        elif (
            numeric_column is not None
            and (
                "lowest" in question_lower
                or "minimum" in question_lower
                or "min" in question_lower
                or "smallest" in question_lower
            )
        ):

            result = working_df[numeric_column].min()

            st.success(
                f"🔻 Lowest {numeric_column}: "
                f"{result:,.2f}"
            )

            min_index = working_df[numeric_column].idxmin()

            min_row = working_df.loc[min_index]

            st.write("📌 Related record:")

            st.dataframe(
                pd.DataFrame([min_row]),
                use_container_width=True
            )

            st.info(
                f"🧠 I searched the {numeric_column} "
                f"column and identified the smallest value."
            )

        # --------------------------------------------------
        # COUNT / HOW MANY
        # --------------------------------------------------

        elif (
            "how many" in question_lower
            or "count" in question_lower
            or "number of" in question_lower
        ):

            if filter_value is not None:

                result = len(working_df)

                st.success(
                    f"🔢 Number of records for "
                    f"{filter_value}: {result}"
                )

                st.info(
                    f"🧠 I filtered {filter_column} for "
                    f"'{filter_value}' and counted the "
                    f"matching records."
                )

            elif group_column is not None:

                grouped_count = (
                    df[group_column]
                    .value_counts()
                )

                st.subheader(
                    f"🔢 Count by {group_column}"
                )

                st.bar_chart(grouped_count)

                st.dataframe(
                    grouped_count.reset_index(
                        name="Count"
                    ),
                    use_container_width=True
                )

            else:

                st.success(
                    f"🔢 Total number of records: {len(df)}"
                )

                st.info(
                    "🧠 I counted the rows in the dataset."
                )

        # --------------------------------------------------
        # TOP / BEST / MOST
        # --------------------------------------------------

        elif (
            numeric_column is not None
            and group_column is not None
            and (
                "top" in question_lower
                or "best" in question_lower
                or "most" in question_lower
            )
        ):

            grouped = (
                df.groupby(group_column)[numeric_column]
                .sum()
                .sort_values(ascending=False)
            )

            top_group = grouped.index[0]
            top_value = grouped.iloc[0]

            st.success(
                f"🏆 {top_group} has the highest "
                f"{numeric_column}: {top_value:,.2f}"
            )

            st.bar_chart(grouped)

            st.dataframe(
                grouped.reset_index(
                    name=f"Total {numeric_column}"
                ),
                use_container_width=True
            )

            st.info(
                f"🧠 I grouped the data by {group_column}, "
                f"calculated total {numeric_column}, "
                f"and sorted the groups from highest to lowest."
            )

        # --------------------------------------------------
        # SIMPLE FILTER QUESTION
        # --------------------------------------------------

        elif (
            filter_value is not None
            and numeric_column is not None
        ):

            result = working_df[numeric_column].sum()

            st.success(
                f"💡 {numeric_column} for "
                f"{filter_value}: {result:,.2f}"
            )

            st.dataframe(
                working_df,
                use_container_width=True
            )

            st.info(
                f"🧠 I found '{filter_value}' in the "
                f"{filter_column} column and displayed "
                f"the matching records."
            )

        # --------------------------------------------------
        # UNKNOWN QUESTION
        # --------------------------------------------------

        else:

            st.warning(
                "🤔 I couldn't understand this question yet."
            )

            st.write(
                "Try questions such as:"
            )

            st.write(
                """
                • What is the total sales?

                • What is the average sales?

                • What is the highest sales?

                • What is the lowest sales?

                • How many laptops are there?

                • What is the total sales of laptop?

                • What is the average sales of laptop?

                • Which product has the highest sales?

                • Which region has the highest sales?

                • Show sales by region
                """
            )