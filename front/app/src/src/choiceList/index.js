import React from 'react';

import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import LinearProgress from '@material-ui/core/LinearProgress';

import { InfiniteLoader, List } from 'react-virtualized';


export default function ChoiceList(props) {
	const remoteRowCount = props.initialData.totalCount;
	const list = props.initialData.wines;

	const isRowLoaded = ({ index }) => {
		return !!list[index];
	}

	const loadMoreRows = ({ startIndex, stopIndex }) => {
		const count = stopIndex - startIndex;
		return fetch(`/api/wines/search?name=${encodeURIComponent(props.initialData.paramLikeName)}&skip=${startIndex}&count=${count}`)
			.then((response) => {
				response.json().then((json) => {
					json.wines?.map((wine) => list.push(wine))
				});
			})
	}

	const rowRenderer = ({ key, index, style}) => {
		return (
			<ListItem
				button
				style={style}
				key={key}
				selected={props.getSelectedWineId() === list[index]?.id}
				onClick={(e) => props.setSelectedWineId(list[index]?.id)}
			>
				<ListItemText
					primary={list[index]?.name}
					secondary={`Millesime ${list[index]?.millesime}`}
				/>
			</ListItem>
		)
	}

	return (
		remoteRowCount
			? <InfiniteLoader
				isRowLoaded={isRowLoaded}
				loadMoreRows={loadMoreRows}
				rowCount={remoteRowCount}
				threshold={10}
			>
				{({ onRowsRendered, registerChild }) => (
					<List
						height={400}
						width={props.width}
						overscanCount={5}
						rowCount={remoteRowCount}
						onRowsRendered={onRowsRendered}
						ref={registerChild}

						rowHeight={80}
						rowRenderer={rowRenderer}
					/>
				)}
			</InfiniteLoader>
			: <LinearProgress />
	);
}