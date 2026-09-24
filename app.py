import streamlit as st
import pandas as pd
import re

# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("📊 Schema-Agnostic Natural Language Data Analyst")

st.write(
    "Upload any CSV or Excel dataset and ask questions "
    "about your data in normal English."
)

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