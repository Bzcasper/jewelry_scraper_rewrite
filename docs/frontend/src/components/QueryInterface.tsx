// frontend/src/components/QueryInterface.tsx
import React, { useState } from 'react';
import { styled } from '@mui/material/styles';
import {
    Paper,
    Typography,
    Grid,
    TextField,
    Select,
    MenuItem,
    Button,
    FormControl,
    InputLabel,
    Slider,
    Chip,
    Box,
    Alert,
    CircularProgress
} from '@mui/material';
import { useQueryConfig } from '../hooks/useQueryConfig';
import { useScrapingJob } from '../hooks/useScrapingJob';

const StyledPaper = styled(Paper)(({ theme }) => ({
    padding: theme.spacing(3),
    marginBottom: theme.spacing(3),
    backgroundColor: theme.palette.background.default,
    boxShadow: theme.shadows[3],
    '&:hover': {
        boxShadow: theme.shadows[6],
    },
    transition: 'box-shadow 0.3s ease-in-out'
}));

const QueryForm = styled('form')(({ theme }) => ({
    '& .MuiTextField-root': {
        marginBottom: theme.spacing(2),
    },
    '& .MuiFormControl-root': {
        marginBottom: theme.spacing(2),
    }
}));

export const QueryInterface: React.FC = () => {
    const { config, updateConfig, resetConfig } = useQueryConfig();
    const { startJob, status, error } = useScrapingJob();
    const [advanced, setAdvanced] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        await startJob(config);
    };

    return (
        <StyledPaper elevation={3}>
            <Typography variant=""h5"" gutterBottom color=""primary"">
                Jewelry Search Configuration
            </Typography>

            <QueryForm onSubmit={handleSubmit}>
                <Grid container spacing={3}>
                    <Grid item xs={12}>
                        <TextField
                            fullWidth
                            label=""Search Query""
                            value={config.query}
                            onChange={(e) => updateConfig('query', e.target.value)}
                            required
                            variant=""outlined""
                            helperText=""Enter keywords for jewelry search""
                        />
                    </Grid>

                    <Grid item xs={12} md={6}>
                        <FormControl fullWidth>
                            <InputLabel>Platform</InputLabel>
                            <Select
                                value={config.platform}
                                onChange={(e) => updateConfig('platform', e.target.value)}
                                label=""Platform""
                            >
                                <MenuItem value=""amazon"">Amazon</MenuItem>
                                <MenuItem value=""ebay"">eBay</MenuItem>
                            </Select>
                        </FormControl>
                    </Grid>

                    <Grid item xs={12} md={6}>
                        <TextField
                            fullWidth
                            type=""number""
                            label=""Maximum Items""
                            value={config.maxItems}
                            onChange={(e) => updateConfig('maxItems', parseInt(e.target.value))}
                            InputProps={{ inputProps: { min: 1, max: 1000 } }}
                        />
                    </Grid>

                    {advanced && (
                        <>
                            <Grid item xs={12}>
                                <Typography gutterBottom>Price Range ($)</Typography>
                                <Slider
                                    value={[config.minPrice || 0, config.maxPrice || 1000]}
                                    onChange={(_, newValue: number[]) => {
                                        updateConfig('minPrice', newValue[0]);
                                        updateConfig('maxPrice', newValue[1]);
                                    }}
                                    valueLabelDisplay=""auto""
                                    min={0}
                                    max={1000}
                                />
                            </Grid>

                            <Grid item xs={12}>
                                <FormControl fullWidth>
                                    <InputLabel>Categories</InputLabel>
                                    <Select
                                        multiple
                                        value={config.categories}
                                        onChange={(e) => updateConfig('categories', e.target.value)}
                                        renderValue={(selected) => (
                                            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                                                {selected.map((value) => (
                                                    <Chip key={value} label={value} />
                                                ))}
                                            </Box>
                                        )}
                                    >
                                        <MenuItem value=""rings"">Rings</MenuItem>
                                        <MenuItem value=""necklaces"">Necklaces</MenuItem>
                                        <MenuItem value=""bracelets"">Bracelets</MenuItem>
                                        <MenuItem value=""earrings"">Earrings</MenuItem>
                                    </Select>
                                </FormControl>
                            </Grid>

                            <Grid item xs={12}>
                                <FormControl fullWidth>
                                    <InputLabel>Condition</InputLabel>
                                    <Select
                                        value={config.condition}
                                        onChange={(e) => updateConfig('condition', e.target.value)}
                                    >
                                        <MenuItem value=""new"">New</MenuItem>
                                        <MenuItem value=""used"">Used</MenuItem>
                                        <MenuItem value=""all"">All</MenuItem>
                                    </Select>
                                </FormControl>
                            </Grid>
                        </>
                    )}

                    <Grid item xs={12}>
                        <Box sx={{ display: 'flex', gap: 2, justifyContent: 'space-between' }}>
                            <Button
                                variant=""outlined""
                                onClick={() => setAdvanced(!advanced)}
                            >
                                {advanced ? 'Hide Advanced' : 'Show Advanced'}
                            </Button>

                            <Box sx={{ display: 'flex', gap: 2 }}>
                                <Button
                                    variant=""outlined""
                                    onClick={resetConfig}
                                    disabled={status === 'loading'}
                                >
                                    Reset
                                </Button>
                                <Button
                                    type=""submit""
                                    variant=""contained""
                                    color=""primary""
                                    disabled={status === 'loading'}
                                    startIcon={status === 'loading' ? <CircularProgress size={20} /> : null}
                                >
                                    {status === 'loading' ? 'Starting...' : 'Start Scraping'}
                                </Button>
                            </Box>
                        </Box>
                    </Grid>

                    {error && (
                        <Grid item xs={12}>
                            <Alert severity=""error"">{error}</Alert>
                        </Grid>
                    )}

                    {status === 'success' && (
                        <Grid item xs={12}>
                            <Alert severity=""success"">
                                Scraping job started successfully! You can monitor the progress below.
                            </Alert>
                        </Grid>
                    )}
                </Grid>
            </QueryForm>
        </StyledPaper>
    );
};