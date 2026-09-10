import { useSelector } from "react-redux";

function Field({ label, value }) {
  return (
    <div className="form-field">
      <label>{label}</label>
      <input value={value || ""} readOnly />
    </div>
  );
}

function ComplaintDetails() {
  const complaint = useSelector(
    (state) => state.complaint.complaint,
  );

  if (!complaint) {
    return (
      <div className="empty-state">
        Upload a complaint document to populate the form.
      </div>
    );
  }

  return (
    <div className="complaint-form">

      <section>
        <h2>1. ORIGIN &amp; CUSTOMER DETAILS</h2>

        <div className="form-grid">
          <Field
            label="Complaint Source"
            value={complaint.complaint_source}
          />

          <Field
            label="Customer Name"
            value={complaint.customer_name}
          />
        </div>
      </section>

      <section>
        <h2>2. PRODUCT &amp; BATCH IDENTIFICATION</h2>

        <div className="form-grid">
          <Field
            label="Product Name"
            value={complaint.product_name}
          />

          <Field
            label="Product Strength"
            value={complaint.product_strength_grade}
          />

          <Field
            label="Batch / Lot Number"
            value={complaint.batch_lot_number}
          />

          <Field
            label="Affected Quantity"
            value={complaint.quantity_affected}
          />

          <Field
            label="Manufacturing Date"
            value={complaint.manufacturing_date}
          />

          <Field
            label="Expiry Date"
            value={complaint.expiry_date}
          />
        </div>
      </section>

      <section>
        <h2>3. FACILITY &amp; MATERIAL IMPACT</h2>

        <div className="form-grid">
            <div className="form-field">
            <label>Originating Site Block</label>

            <select
                value={complaint.originating_site_block || ""}
                disabled
            >
                <option value="">
                Not identified
                </option>

                {complaint.originating_site_block && (
                <option value={complaint.originating_site_block}>
                    {complaint.originating_site_block}
                </option>
                )}
            </select>
            </div>

            <Field
            label="Impacted Non-Product Materials (NPM)"
            value={
                complaint.impacted_non_product_materials ||
                "Not identified"
            }
            />
        </div>
      </section>

      <section>
        <h2>4. DEFECT ANALYSIS</h2>

        <Field
          label="Complaint Category"
          value={complaint.complaint_type}
        />

        <div className="form-field description-field">
          <label>Complaint Description</label>

          <textarea
            value={
              complaint.detailed_complaint_description || ""
            }
            readOnly
          />
        </div>
      </section>
    </div>
  );
}

export default ComplaintDetails;