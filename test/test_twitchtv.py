from twitch import *
import unittest
import logging

class TestTwitchTV(unittest.TestCase):
    TwitchTV = None

    def setUp(self):
        #setup resolver
        self.twitch = TwitchTV(logging) 

    def tearDown(self):
        self.twitch = None

    def test_playback(self):
        featured = self.twitch.getFeaturedStream()
        featured = featured[0]['stream']['channel']['name']
        logging.debug("found featured stream: " + featured)
        featuredUrl = self.twitch.getLiveStream(featured, 0)
        self.assertIn('http://',featuredUrl)

    def test_get_channels(self):
        channels = self.twitch.getChannels()
        channels = channels[0]['channel']['name']
        logging.debug("found channel: " + channels)
        channelsurl = self.twitch.getLiveStream(channels, 0)
        self.assertIn('http://',channelsurl)

    def test_unavailable_channel(self):
        featured = self.twitch.getFeaturedStream()
        featured = featured[0]['stream']['channel']['name'] + "13456789152318561"
        logging.debug("testing non available stream: " + featured)
        with self.assertRaises(TwitchException) as context:
            self.twitch.getLiveStream(featured, 0)
        self.assertEqual(context.exception.code, TwitchException.HTTP_ERROR)

    def test_offline_channel(self):
        offlinechannel = "winlu"
        logging.debug("testing offline stream: " + offlinechannel)
        with self.assertRaises(TwitchException) as context:
            self.twitch.getLiveStream(offlinechannel, 0)
        self.assertEqual(context.exception.code, TwitchException.STREAM_OFFLINE)

    def test_get_games_streams(self):
        result = self.twitch.getGames(offset=0, limit=10)
        channels = self.twitch.getGameStreams(result[0]['game']['name'], offset=0, limit=10)
        url = self.twitch.getLiveStream(channels[0]['channel']['name'], 0)
        self.assertIn('http://',url)

    def test_get_teams_streams(self):#define fail state
        teams = self.twitch.getTeams(index=0)
        team = teams[0]['name']
        teamstreams = self.twitch.getTeamStreams(team)

    def test_search_streams(self):
        featured = self.twitch.getFeaturedStream()
        featured = featured[0]['stream']['channel']['name']
        result = []
        result = self.twitch.searchStreams(featured,offset=0, limit=10)
        self.assertNotEqual([],result)

    def test_following_channels(self):
        following = []
        following = self.twitch.getFollowingStreams("winlu")
        self.assertNotEqual([],following)

    def test_following_videos(self):
        channelname = "Ellohime"
        following = self.twitch.getFollowerVideos(channelname, offset=0, past=True)
        self.assertTrue(following['_total'] > 0,"total is not bigger then 0")

    def test_video_playlist_chunked(self):
        videoid = 'c5928479'
        expected_playlist = [
            ('', ('', 'http://static-cdn.jtvnw.net/jtv.thumbs/archive-613890547-320x240.jpg')),
            ('http://media-cdn.twitch.tv/store24.media78/archives/2015-1-20/live_user_cobaltstreak_1421794812.flv', ('Resident Evil 1 HD Remaster - Part One - Part 1 of 13', 'http://static-cdn.jtvnw.net/jtv.thumbs/archive-613890547-320x240.jpg')),
            ('http://media-cdn.twitch.tv/store60.media52/archives/2015-1-20/live_user_cobaltstreak_1421796525.flv', ('Resident Evil 1 HD Remaster - Part One - Part 2 of 13', 'http://static-cdn.jtvnw.net/jtv.thumbs/archive-613890547-320x240.jpg')),
            ('http://media-cdn.twitch.tv/store143.media96/archives/2015-1-20/live_user_cobaltstreak_1421798235.flv', ('Resident Evil 1 HD Remaster - Part One - Part 3 of 13', 'http://static-cdn.jtvnw.net/jtv.thumbs/archive-613890547-320x240.jpg')),
            ('http://media-cdn.twitch.tv/store57.media71/archives/2015-1-21/live_user_cobaltstreak_1421799946.flv', ('Resident Evil 1 HD Remaster - Part One - Part 4 of 13', 'http://static-cdn.jtvnw.net/jtv.thumbs/archive-613890547-320x240.jpg')),
            ('http://media-cdn.twitch.tv/store111.media73/archives/2015-1-21/live_user_cobaltstreak_1421801656.flv', ('Resident Evil 1 HD Remaster - Part One - Part 5 of 13', 'http://static-cdn.jtvnw.net/jtv.thumbs/archive-613890547-320x240.jpg')),
            ('http://media-cdn.twitch.tv/store123.media87/archives/2015-1-21/live_user_cobaltstreak_1421803367.flv', ('Resident Evil 1 HD Remaster - Part One - Part 6 of 13', 'http://static-cdn.jtvnw.net/jtv.thumbs/archive-613890547-320x240.jpg')),
            ('http://media-cdn.twitch.tv/store130.media90/archives/2015-1-21/live_user_cobaltstreak_1421805077.flv', ('Resident Evil 1 HD Remaster - Part One - Part 7 of 13', 'http://static-cdn.jtvnw.net/jtv.thumbs/archive-613890547-320x240.jpg')),
            ('http://media-cdn.twitch.tv/store147.media98/archives/2015-1-21/live_user_cobaltstreak_1421806789.flv', ('Resident Evil 1 HD Remaster - Part One - Part 8 of 13', 'http://static-cdn.jtvnw.net/jtv.thumbs/archive-613890547-320x240.jpg')),
            ('http://media-cdn.twitch.tv/store70.media57/archives/2015-1-21/live_user_cobaltstreak_1421808499.flv', ('Resident Evil 1 HD Remaster - Part One - Part 9 of 13', 'http://static-cdn.jtvnw.net/jtv.thumbs/archive-613890547-320x240.jpg')),
            ('http://media-cdn.twitch.tv/store161.media105/archives/2015-1-21/live_user_cobaltstreak_1421810210.flv', ('Resident Evil 1 HD Remaster - Part One - Part 10 of 13', 'http://static-cdn.jtvnw.net/jtv.thumbs/archive-613890547-320x240.jpg')),
            ('http://media-cdn.twitch.tv/store92.media67/archives/2015-1-21/live_user_cobaltstreak_1421811920.flv', ('Resident Evil 1 HD Remaster - Part One - Part 11 of 13', 'http://static-cdn.jtvnw.net/jtv.thumbs/archive-613890547-320x240.jpg')),
            ('http://media-cdn.twitch.tv/store91.media67/archives/2015-1-21/live_user_cobaltstreak_1421813631.flv', ('Resident Evil 1 HD Remaster - Part One - Part 12 of 13', 'http://static-cdn.jtvnw.net/jtv.thumbs/archive-613890547-320x240.jpg')),
            ('http://media-cdn.twitch.tv/store82.media62/archives/2015-1-21/live_user_cobaltstreak_1421815341.flv', ('Resident Evil 1 HD Remaster - Part One - Part 13 of 13', 'http://static-cdn.jtvnw.net/jtv.thumbs/archive-613890547-320x240.jpg'))
        ]
        playlist = self.twitch.getVideoPlaylist(videoid, 0)
        self.assertEqual(playlist, expected_playlist)

    def test_video_playlist_nonchunked(self):
        videoid = 'v3724525'
        playlist = self.twitch.getVideoPlaylist(videoid, 0)
        self.assertIn(('http://vod.ak.hls.ttvnw.net/v1/AUTH_system/vods_0a81/adwcta_12836574160_195555824/chunked/index-0000000029-19kL.ts?start_offset=0&end_offset=1095663',()), playlist)

    def suite(self):
        testSuite = unittest.TestSuite()
        testSuite.addTest(unittest.makeSuite(TestResolver))
        return testSuite

