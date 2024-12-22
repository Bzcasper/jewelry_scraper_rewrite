// frontend/src/features/scraping/ScrapingForm.tsx
import React from 'react';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { 
  TextField, 
  Button, 
  Select, 
  MenuItem, 
  FormControl,
  InputLabel,
  Grid,
  Paper
} from '@mui/material';
import { useAppDispatch, useAppSelector } from '../../store/hooks';
import { startScraping } from '../../services/scraping';

const schema = yup.object({
  query: yup.string().required('Search query is required'),
  platform: yup.string().oneOf(['ebay', 'amazon']).required(),
  maxItems: yup.number().min(1).max(1000).required(),
  minPrice: yup.number().min(0),
  maxPrice: yup.number().min(0),
  category: yup.string()
}).required();

interface ScrapingFormData {
  query: string;
  platform: 'ebay' | 'amazon';
  maxItems: number;
  minPrice?: number;
  maxPrice?: number;
  category?: string;
}

export const ScrapingForm: React.FC = () => {
  const dispatch = useAppDispatch();
  const { isLoading } = useAppSelector(state => state.scraping);
  
  const { register, handleSubmit, formState: { errors } } = useForm<ScrapingFormData>({
    resolver: yupResolver(schema)
  });

  const onSubmit = async (data: ScrapingFormData) => {
    try {
      await dispatch(startScraping(data)).unwrap();
    } catch (error) {
      console.error('Failed to start scraping:', error);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <form onSubmit={handleSubmit(onSubmit)}>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label=""Search Query""
              {...register('query')}
              error={!!errors.query}
              helperText={errors.query?.message}
            />
          </Grid>
          
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth>
              <InputLabel>Platform</InputLabel>
              <Select
                {...register('platform')}
                error={!!errors.platform}
              >
                <MenuItem value=""ebay"">eBay</MenuItem>
                <MenuItem value=""amazon"">Amazon</MenuItem>
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              type=""number""
              label=""Max Items""
              {...register('maxItems')}
              error={!!errors.maxItems}
              helperText={errors.maxItems?.message}
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              type=""number""
              label=""Min Price""
              {...register('minPrice')}
              error={!!errors.minPrice}
              helperText={errors.minPrice?.message}
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              type=""number""
              label=""Max Price""
              {...register('maxPrice')}
              error={!!errors.maxPrice}
              helperText={errors.maxPrice?.message}
            />
          </Grid>

          <Grid item xs={12}>
            <Button
              fullWidth
              variant=""contained""
              type=""submit""
              disabled={isLoading}
            >
              {isLoading ? 'Starting...' : 'Start Scraping'}
            </Button>
          </Grid>
        </Grid>
      </form>
    </Paper>
  );
};