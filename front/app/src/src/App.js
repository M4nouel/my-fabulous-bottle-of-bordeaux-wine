
import React, { useState, useCallback } from 'react';
import { useQuery } from "react-query";
import debounce from 'lodash.debounce';

import ChoiceList from './choiceList';
import NeighbhorsTable from './neighbhorsTable';

import { makeStyles } from '@material-ui/core/styles';
import LinearProgress from '@material-ui/core/LinearProgress';
import MuiAlert from '@material-ui/lab/Alert';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import Paper from '@material-ui/core/Paper';
import Box from '@material-ui/core/Box';



const useStyles = makeStyles((theme) => ({
	root: {
		padding: '20px',
		minHeight: '60%',
		minWidth: '80%',
	},
	paper: {
		padding: theme.spacing(2),
		minWidth: '80%',

		background: 'linear-gradient(45deg, #007eff5c 30%, #21cbf329 90%)',
		border: 0,
		borderRadius: 3,
		boxShadow: '0 3px 5px 2px #33333380',
	},
	form: {
		flexDirection: 'row',
		justifyContent: 'space-around',
	}
}));


const App = () => {
	const [name, setName] = useState("");
	const [nbNeighborsToFetch, setNbNeighborsToFetch] = useState(10);

	const [selectedWineId, setSelectedWineId] = useState(null);
	const lazyGetSelectedWineId = () => selectedWineId;

	const { data = [], error, status } = useQuery(
		["wines", name],
		async () => await (await fetch(`/api/wines/search?name=${encodeURIComponent(name)}&skip=0&count=50`)).json()
	);

	// eslint-disable-next-line
	const debouncedName = useCallback(
		debounce(
			(val) => setName(val),
			1000
		),
		[]
	);

	const classes = useStyles();

	return (
		<Grid container direction="row" justifyContent="center" alignItems="center" className={classes.root}>
		<Paper elevation={3} className={classes.paper}>
		<Grid container direction="row" justifyContent="space-evenly" alignItems="flex-start">
			{
				status === "error" &&
				<MuiAlert elevation={6} variant="filled" severity="error">
					Internal error ! ({error.message})
				</MuiAlert>
			}
			{status === "loading" && <LinearProgress />}

			<Grid item xs={6}>
				<FormControl fullWidth variant="outlined" className={classes.form}>
					<Box width="73%">
						<TextField
							label="Name"
							fullWidth
							variant="outlined"
							onChange={(e) => debouncedName(e.target.value)}
						/>
					</Box>
					<Box width="23%">
						<Select
							id="nb-similar-wine-to-fetch"
							value={nbNeighborsToFetch}
							onChange={(e) => setNbNeighborsToFetch(e.target.value)}
						>
							{
								Array(10).fill(0).map((e, index) => {
									return <MenuItem key={index} value={index + 1}>{index + 1}</MenuItem>
								})
							}
						</Select>
					</Box>
				</FormControl>
				<Box className={classes.list} width={420}>
					<ChoiceList

						width={420}
						initialData={data}
						setSelectedWineId={setSelectedWineId}
						getSelectedWineId={lazyGetSelectedWineId}
					/>
				</Box>
			</Grid>

			<Grid item xs={6}>
				<NeighbhorsTable
					nbNeighborsToFetch={nbNeighborsToFetch}
					selectedWineId={selectedWineId}
				/>
			</Grid>
		</Grid>
		</Paper>
		</Grid>
	);
}

export default App;