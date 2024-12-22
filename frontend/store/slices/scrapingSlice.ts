// frontend/src/store/slices/scrapingSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface ScrapingState {
  activeJobs: Record<string, ScrapingJob>;
  isLoading: boolean;
  error: string | null;
}

interface ScrapingJob {
  id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  itemsScraped: number;
  error?: string;
}

const initialState: ScrapingState = {
  activeJobs: {},
  isLoading: false,
  error: null
};

const scrapingSlice = createSlice({
  name: 'scraping',
  initialState,
  reducers: {
    startScraping: (state) => {
      state.isLoading = true;
      state.error = null;
    },
    scrapingSuccess: (state, action: PayloadAction<{ jobId: string }>) => {
      state.isLoading = false;
      state.activeJobs[action.payload.jobId] = {
        id: action.payload.jobId,
        status: 'running',
        progress: 0,
        itemsScraped: 0
      };
    },
    updateJobStatus: (state, action: PayloadAction<ScrapingJob>) => {
      state.activeJobs[action.payload.id] = action.payload;
    },
    scrapingError: (state, action: PayloadAction<string>) => {
      state.isLoading = false;
      state.error = action.payload;
    }
  }
});

export const { startScraping, scrapingSuccess, updateJobStatus, scrapingError } = scrapingSlice.actions;
export default scrapingSlice.reducer;