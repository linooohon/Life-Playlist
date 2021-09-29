function deletePlaylistItem(playlistItemId) {
    fetch("/delete-playlist-item", {
        method: "POST",
        body: JSON.stringify({ playlistItemId: playlistItemId }),
    }).then((_res) => {
        window.location.href = "/app";
    });
}

if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}