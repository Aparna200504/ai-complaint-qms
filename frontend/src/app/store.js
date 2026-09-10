import { configureStore } from "@reduxjs/toolkit";
import complaintReducer from "../features/complaint/complaintSlice";

export const store = configureStore({
  reducer: {
    complaint: complaintReducer,
  },
});