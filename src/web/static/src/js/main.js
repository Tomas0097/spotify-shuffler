
window.showPlaylistTracks = async function (playlistId) {
	async function getPlaylistData(playlistId) {
		const response = await fetch(`/get-playlist/${playlistId}/`)
		if (!response.ok) {throw new Error(`HTTP error! status: ${response.status}`)}
		return await response.json();
	}
	const playlistData = await getPlaylistData(playlistId)
	const playlistTracksContainerElement = document.querySelector('.playlist-tracks-container');

	const playlistTracksUlElement = document.createElement("ul");
	playlistTracksUlElement.classList.add('playlist-tracks-list')

	if (playlistTracksContainerElement.innerHTML) {
		playlistTracksContainerElement.innerHTML = ''
	}

	playlistData.tracks.items.forEach(track => {
		const trackName = track.track.name;
		const trackArtistNamesArray = track.track.artists.map((artist) => artist.name);
		const trackArtistNames = trackArtistNamesArray.join(', ');
		const trackLiElement = document.createElement("li");
		trackLiElement.textContent = trackArtistNames + ' --- ' + trackName

		playlistTracksUlElement.append(trackLiElement)
	})

	playlistTracksContainerElement.append(playlistTracksUlElement)
};
