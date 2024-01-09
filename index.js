<script>
   $(document).ready(function() {
      $('.movie-item').each(function() {
         var $movie = $(this);
         if (movie){
            console.log(movie.attr('id'));
            var $moviePosterContainer= $movie.find('.movie-poster-contianer');
            if ($moviePosterContainer && $moviePosterContainer.length > 0) {
                var $movieInfos = $moviePosterContainer.find('.infos');
                var $moviePoster = $moviePosterContainer.find('.movie-poster img');
                if (!$moviePoster.attr('src')) {
                $movieInfos.css('opacity', '1');
                }
            }
         }
      })
   });
</script>
