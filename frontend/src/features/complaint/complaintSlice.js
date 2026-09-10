import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  filename: null,
  fileType: null,
  extractedText: null,
  complaint: null,
  validation: null,
  riskAssessment: null,
  loading: false,
  error: null,
  committed: false,
  commitId: null,
  commitMessage: null,
};

const complaintSlice = createSlice({
  name: "complaint",
  initialState,
  reducers: {
    setProcessing: (state) => {
      state.loading = true;
      state.error = null;
    },

    setComplaintResult: (state, action) => {
      state.loading = false;
      state.error = null;
      state.committed = false;
      state.commitId = null;
      state.commitMessage = null;

      state.filename = action.payload.filename;
      state.fileType = action.payload.file_type;
      state.extractedText = action.payload.extracted_text;
      state.complaint = action.payload.complaint;
      state.validation = action.payload.validation;
      state.riskAssessment = action.payload.risk_assessment;
    },

    setEditedComplaint: (state, action) => {
      state.loading = false;
      state.error = null;
      state.committed = false;
      state.commitId = null;
      state.commitMessage = null;
      state.complaint = action.payload.updated_form;
      state.validation = action.payload.validation;
      state.riskAssessment = action.payload.risk_assessment;
    },

    setCommitted: (state, action) => {
      state.committed = true;
      state.commitId = action.payload.record.id;
      state.commitMessage = action.payload.message;
      state.error = null;
    },

    setComplaintError: (state, action) => {
      state.loading = false;
      state.error = action.payload;
    },

    resetComplaint: () => initialState,
  },
});

export const {
  setProcessing,
  setComplaintResult,
  setEditedComplaint,
  setCommitted,
  setComplaintError,
  resetComplaint,
} = complaintSlice.actions;

export default complaintSlice.reducer;