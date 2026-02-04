import streamlit as st
import json
from classifier import classify_po

st.set_page_config(page_title="PO Category Classifier", layout="centered")

st.title("📦 PO L1–L2–L3 Classifier")

po_description = st.text_area("PO Description", height=120)
supplier = st.text_input("Supplier (optional)")

if st.button("Classify"):
    if not po_description.strip():
        st.warning("Please enter a PO description.")
    else:
        with st.spinner("Classifying..."):
            result = classify_po(po_description, supplier)

        # ✅ Handle empty / None response safely
        if result is None or str(result).strip() == "":
            st.error("No response received from the model.")
        else:
            # ✅ Try parsing JSON safely
            try:
                parsed_result = json.loads(result)
                st.json(parsed_result)
            except Exception:
                # ✅ Show raw output instead of crashing
                st.error("Model response is not valid JSON.")
                st.subheader("Raw model output")
                st.code(result)
