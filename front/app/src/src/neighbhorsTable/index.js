import React from 'react';
import { useQuery } from "react-query";

import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

import LinearProgress from '@material-ui/core/LinearProgress';
import MuiAlert from '@material-ui/lab/Alert';


export default function NeighbhorsTable(props) {

	const { data = [], error, status } = useQuery(
		["neighbhors", props.selectedWineId, props.nbNeighborsToFetch],
		async () => {
			return Number.isInteger(props.selectedWineId)
				? await (
					await fetch(
						`http://localhost/api/wines/kneighbors/id/${props.selectedWineId}?limit=${props.nbNeighborsToFetch}`
					))
					.json()
				: []
		}
	);

	return (
		<TableContainer component={Paper}>
			<Table aria-label="simple table">
				<TableHead>
					<TableRow>
						<TableCell>Name</TableCell>
						<TableCell align="right">Millesime</TableCell>
					</TableRow>
				</TableHead>
				<TableBody>
					{data?.map((row) => (
						<TableRow
							key={row.id}
							selected={props.selectedWineId === row.id}
						>
							<TableCell component="th" scope="row">
								{row.name}
							</TableCell>
							<TableCell align="right">
								{row.millesime}
							</TableCell>
						</TableRow>
					))}
				</TableBody>
			</Table>
			{
				status === "error" &&
				<MuiAlert elevation={6} variant="filled" severity="error">
					Internal error ! ({error.message})
				</MuiAlert>
			}
			{status === "loading" && <LinearProgress />}
		</TableContainer>
	);
}