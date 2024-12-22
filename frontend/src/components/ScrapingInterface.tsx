// frontend/src/components/ScrapingInterface.tsx
import React, { useState } from 'react';
import { 
    Button, 
    TextField, 
    Select, 
    MenuItem, 
    FormControl,
    InputLabel,
    Grid,
    Paper,
    Typography
} from '@mui/material';
import { useQuery, useMutation } from 'react-query';
import { startScraping, getScrapingStatus } from '../services/api';

interface ScrapingParams {
    query: string;
    platform: 'ebay' | 'amazon';
    maxItems: number;
    category?: string;
    minPrice?: number;
    maxPrice?: number;
    condition?: 'new' | 'used' | 'all';
}

export const ScrapingInterface: React.FC = () => {
    const [params, setParams] = useState<ScrapingParams>({
        query: '',
        platform: 'ebay',
        maxItems: 100,
        condition: 'all'
    });

    const [jobId, setJobId] = useState<string | null>(null);

    const { mutate: startScrapingJob, isLoading } = useMutation(startScraping, {
        onSuccess: (data) => {
            setJobId(data.jobId);
        }
    });

    const { data: jobStatus } = useQuery(
        ['scrapingStatus', jobId],
        () => getScrapingStatus(jobId!),
        {
            enabled: !!jobId,
            refetchInterval: 5000 // Poll every 5 seconds
        }
    );

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        startScrapingJob(params);
    };

    return (
        <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant=""h5"" gutterBottom>
                Scrape Jewelry Data
            </Typography>
            
            <form onSubmit={handleSubmit}>
                <Grid container spacing={2}>
                    <Grid item xs={12}>
                        <TextField
                            fullWidth
                            label=""Search Query""
                            value={params.query}
                            onChange={(e) => setParams({...params, query: e.target.value})}
                            required
                        />
                    </Grid>

                    <Grid item xs={12} sm={6}>
                        <FormControl fullWidth>
                            <InputLabel>Platform</InputLabel>
                            <Select
                                value={params.platform}
                                onChange={(e) => setParams({...params, platform: e.target.value as 'ebay' | 'amazon'})}
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
                            value={params.maxItems}
                            onChange={(e) => setParams({...params, maxItems: parseInt(e.target.value)})}
                            InputProps={{ inputProps: { min: 1, max: 1000 } }}
                        />
                    </Grid>

                    {/* Add more filter fields here */}

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

            {jobId && jobStatus && (
                <Paper sx={{ mt: 2, p: 2 }}>
                    <Typography variant=""h6"">Scraping Status</Typography>
                    <Typography>Status: {jobStatus.status}</Typography>
                    <Typography>Progress: {jobStatus.progress}%</Typography>
                    <Typography>Items Found: {jobStatus.itemsFound}</Typography>
                    {jobStatus.error && (
                        <Typography color=""error"">Error: {jobStatus.error}</Typography>
                    )}
                </Paper>
            )}
        </Paper>
    );
};
interface DashboardState {
    activeScrapes: number;
    productsFound: number;
    quality: {
    highQuality: number;
    mediumQuality: number;
    lowQuality: number;
    };
    performance: {
    successRate: number;
    averageTime: number;
    };
    }

    class DashboardManager {
        updateMetrics(metrics: DashboardState): void {
        # Update UI in real-time
        # Show trends and patterns
        }
}
interface SearchOptions {
    priceRange: [number, number];
    categories: string[];
    materials: string[];
    quality: 'high' | 'medium' | 'low';
    sortBy: 'price' | 'quality' | 'date';
    }
    
class AdvancedSearch {
    async searchProducts(options: SearchOptions): Promise<Product[]> {
    # Implement advanced filtering
    # Sort and rank results
    }
    }