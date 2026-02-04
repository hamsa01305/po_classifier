import json
import streamlit as st
from classifier import classify_po

PAGE_TITLE = "PO Category Classifier"
LAYOUT = "centered"
DESCRIPTION_LABEL = "PO Description"
SUPPLIER_LABEL = "Supplier"
DESCRIPTION_HELP = "Describe the purchase order. This is required."
SUPPLIER_HELP = "Optional. Helps improve classification when available."

st.set_page_config(page_title=PAGE_TITLE, layout=LAYOUT)
st.title("📦 PO L1–L2–L3 Classifier")

if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "last_raw" not in st.session_state:
    st.session_state.last_raw = None

with st.form("classifier_form", clear_on_submit=False):
    po_description = st.text_area(
        DESCRIPTION_LABEL,
        height=120,
        help=DESCRIPTION_HELP,
        placeholder="Example: 500 units of nitrile gloves for warehouse operations",
    )
    supplier = st.text_input(SUPPLIER_LABEL, help=SUPPLIER_HELP)
    submitted = st.form_submit_button("Classify")

if submitted:
    if not po_description.strip():
        st.warning("Please enter a PO description.")
    else:
        try:
            with st.spinner("Classifying..."):
                result = classify_po(po_description, supplier)
        except Exception as exc:
            st.error("Classification failed. Please try again.")
            st.exception(exc)
        else:
            st.session_state.last_raw = result
            try:
                st.session_state.last_result = json.loads(result)
            except Exception:
                st.session_state.last_result = None

if st.session_state.last_result is not None:
    st.subheader("Result")
    st.json(st.session_state.last_result)
elif st.session_state.last_raw:
    st.subheader("Result")
    st.error("Invalid model response")
    with st.expander("Show raw response"):
        st.text(st.session_state.last_raw)
