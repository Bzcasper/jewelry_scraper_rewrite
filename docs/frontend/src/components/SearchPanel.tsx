// frontend/src/components/SearchPanel.tsx
import React from 'react';
import { 
    Paper, 
    TextField, 
    Select, 
    MenuItem, 
    Button, 
    Grid, 
    FormControl,
    InputLabel,
    Typography
} from '@mui/material';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';

const searchSchema = z.object({
    query: z.string().min(1, 'Search query is required'),
    platform: z.enum(['amazon', 'ebay']),
    maxItems: z.number().min(1).max(1000),
    minPrice: z.number().min(0).optional(),
    maxPrice: z.number().min(0).optional(),
    category: z.string().optional()
});

type SearchFormData = z.infer<typeof searchSchema>;

interface SearchPanelProps {
    onSearch: (data: SearchFormData) => void;
    isLoading: boolean;
}

export const SearchPanel: React.FC<SearchPanelProps> = ({ onSearch, isLoading }) => {
    const { control, handleSubmit, formState: { errors } } = useForm<SearchFormData>({
        resolver: zodResolver(searchSchema),
        defaultValues: {
            platform: 'amazon',
            maxItems: 100
        }
    });

    return (
        <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
            <Typography variant=""h6"" gutterBottom>
                Search Jewelry
            </Typography>
            
            <form onSubmit={handleSubmit(onSearch)}>
                <Grid container spacing={2}>
                    <Grid item xs={12}>
                        <Controller
                            name=""query""
                            control={control}
                            render={({ field }) => (
                                <TextField
                                    {...field}
                                    fullWidth
                                    label=""Search Query""
                                    error={!!errors.query}
                                    helperText={errors.query?.message}
                                />
                            )}
                        />
                    </Grid>

                    <Grid item xs={12} sm={6}>
                        <FormControl fullWidth>
                            <InputLabel>Platform</InputLabel>
                            <Controller
                                name=""platform""
                                control={control}
                                render={({ field }) => (
                                    <Select {...field} label=""Platform"">
                                        <MenuItem value=""amazon"">Amazon</MenuItem>
                                        <MenuItem value=""ebay"">eBay</MenuItem>
                                    </Select>
                                )}
                            />
                        </FormControl>
                    </Grid>

                    <Grid item xs={12} sm={6}>
                        <Controller
                            name=""maxItems""
                            control={control}
                            render={({ field }) => (
                                <TextField
                                    {...field}
                                    fullWidth
                                    type=""number""
                                    label=""Max Items""
                                    error={!!errors.maxItems}
                                    helperText={errors.maxItems?.message}
                                />
                            )}
                        />
                    </Grid>

                    <Grid item xs={12} sm={6}>
                        <Controller
                            name=""minPrice""
                            control={control}
                            render={({ field }) => (
                                <TextField
                                    {...field}
                                    fullWidth
                                    type=""number""
                                    label=""Min Price""
                                    error={!!errors.minPrice}
                                    helperText={errors.minPrice?.message}
                                />
                            )}
                        />
                    </Grid>

                    <Grid item xs={12} sm={6}>
                        <Controller
                            name=""maxPrice""
                            control={control}
                            render={({ field }) => (
                                <TextField
                                    {...field}
                                    fullWidth
                                    type=""number""
                                    label=""Max Price""
                                    error={!!errors.maxPrice}
                                    helperText={errors.maxPrice?.message}
                                />
                            )}
                        />
                    </Grid>

                    <Grid item xs={12}>
                        <Button
                            type=""submit""
                            variant=""contained""
                            color=""primary""
                            fullWidth
                            disabled={isLoading}
                        >
                            {isLoading ? 'Searching...' : 'Search'}
                        </Button>
                    </Grid>
                </Grid>
            </form>
        </Paper>
    );
};