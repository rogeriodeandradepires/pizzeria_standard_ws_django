( function( $, elementorFrontend ) {

	'use strict';

	var JetReviews = {

		init: function() {

			var widgets = {
				'jet-reviews.default' : JetReviews.widgetJetReviews
			};

			$.each( widgets, function( widget, callback ) {
				elementorFrontend.hooks.addAction( 'frontend/element_ready/' + widget, callback );
			});

		},

		widgetJetReviews: function( $scope ) {
			var $target       = $scope.find( '.jet-review' ),
				settings      = $target.data( 'settings' ),
				$form         = $( '.jet-review__form', $target ),
				$submitButton = $( '.jet-review__form-submit', $target ),
				$removeButton = $( '.jet-review__item-remove', $target ),
				$message      = $( '.jet-review__form-message', $target ),
				$rangeControl = $( '.jet-review__form-field.type-range input', $target ),
				ajaxRequest   = null;

			$rangeControl.on( 'input', function( event ) {
				var $this         = $( this ),
					$parent       = $this.closest( '.jet-review__form-field' ),
					$currentValue = $( '.current-value', $parent ),
					value         = $this.val();

					$currentValue.html( value );
			} );

			$submitButton.on( 'click.widgetJetReviews', function() {
				addReviewHandle();

				return false;
			} );

			$removeButton.on( 'click.widgetJetReviews', function() {
				var $this = $( this );

				removeReviewHandle( $this );

				return false;
			} );

			function addReviewHandle() {
				var now            = new Date(),
					reviewTime     = now.getTime(),
					reviewDate     = new Date( reviewTime ).toLocaleString(),
					sendData       = {
						'post_id': settings['post_id'],
						'review_time': reviewTime,
						'review_date': reviewDate
					},
					serializeArray = $form.serializeObject();

				sendData = jQuery.extend( sendData, serializeArray );

				ajaxRequest = jQuery.ajax( {
					type: 'POST',
					url: window.jetReviewData.ajax_url,
					data: {
						'action': 'jet_reviews_add_review',
						'data': sendData
					},
					beforeSend: function( jqXHR, ajaxSettings ) {
						if ( null !== ajaxRequest ) {
							ajaxRequest.abort();
						}

						$submitButton.addClass( 'load-state' );
					},
					error: function( jqXHR, ajaxSettings ) {

					},
					success: function( data, textStatus, jqXHR ) {

						var responseType = data['type'],
							message      = data.message || '';

						if ( 'error' === responseType ) {
							$submitButton.removeClass( 'load-state' );
							$message.addClass( 'visible-state' );

							$( 'span', $message ).html( message );
						}

						if ( 'success' === responseType ) {
							location.reload();
						}
					}
				} );
			};

			function removeReviewHandle( $removeButton ) {
				var sendData       = {
						'post_id': settings['post_id'],
					};

				ajaxRequest = jQuery.ajax( {
					type: 'POST',
					url: window.jetReviewData.ajax_url,
					data: {
						'action': 'jet_reviews_remove_review',
						'data': sendData
					},
					beforeSend: function( jqXHR, ajaxSettings ) {
						if ( null !== ajaxRequest ) {
							ajaxRequest.abort();
						}

						$removeButton.addClass( 'load-state' );
					},
					error: function( jqXHR, ajaxSettings ) {

					},
					success: function( data, textStatus, jqXHR ) {
						var successType   = data.type,
							message       = data.message || '';

						if ( 'error' == successType ) {

						}

						if ( 'success' == successType ) {
							location.reload();
						}
					}
				} );
			};
		}
	};

	$( window ).on( 'elementor/frontend/init', JetReviews.init );

	$.fn.serializeObject = function(){

		var self = this,
			json = {},
			push_counters = {},
			patterns = {
				"validate": /^[a-zA-Z][a-zA-Z0-9_-]*(?:\[(?:\d*|[a-zA-Z0-9_-]+)\])*$/,
				"key":      /[a-zA-Z0-9_-]+|(?=\[\])/g,
				"push":     /^$/,
				"fixed":    /^\d+$/,
				"named":    /^[a-zA-Z0-9_-]+$/
			};

		this.build = function(base, key, value){
			base[key] = value;
			return base;
		};

		this.push_counter = function(key){
			if(push_counters[key] === undefined){
				push_counters[key] = 0;
			}
			return push_counters[key]++;
		};

		$.each($(this).serializeArray(), function(){
			// skip invalid keys
			if(!patterns.validate.test(this.name)){
				return;
			}

			var k,
				keys = this.name.match(patterns.key),
				merge = this.value,
				reverse_key = this.name;

			while((k = keys.pop()) !== undefined){

				// adjust reverse_key
				reverse_key = reverse_key.replace(new RegExp("\\[" + k + "\\]$"), '');

				// push
				if(k.match(patterns.push)){
					merge = self.build([], self.push_counter(reverse_key), merge);
				}

				// fixed
				else if(k.match(patterns.fixed)){
					merge = self.build([], k, merge);
				}

				// named
				else if(k.match(patterns.named)){
					merge = self.build({}, k, merge);
				}
			}

			json = $.extend(true, json, merge);
		});

		return json;
	};

}( jQuery, window.elementorFrontend ) );
