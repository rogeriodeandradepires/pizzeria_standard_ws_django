( function( $, elementor ) {

	'use strict';

	var JetParallax = {

		init: function() {
			elementor.hooks.addAction( 'frontend/element_ready/section', JetParallax.elementorSection );
		},

		elementorSection: function( $scope ) {
			var $target   = $scope,
				instance  = null,
				editMode  = Boolean( elementor.isEditMode() );

			instance = new jetSectionParallaxPlugin( $target );
			instance.init();
		},


	};

	$( window ).on( 'elementor/frontend/init', JetParallax.init );

	window.jetSectionParallaxPlugin = function( $target ) {
		var self             = this,
			sectionId        = $target.data('id'),
			settings         = false,
			editMode         = Boolean( elementor.isEditMode() ),
			$window          = $( window ),
			$body            = $( 'body' ),
			scrollLayoutList = [],
			mouseLayoutList  = [],
			winScrollTop     = $window.scrollTop(),
			winHeight        = $window.height(),
			requesScroll     = null,
			requestMouse     = null,
			tiltx            = 0,
			tilty            = 0,
			isSafari         = !!navigator.userAgent.match(/Version\/[\d\.]+.*Safari/),
			platform         = navigator.platform;

		/**
		 * Init
		 */
		self.init = function() {

			if ( ! editMode ) {
				settings = jetParallax[ 'jetParallaxPluginSections' ][ sectionId ] || false;
			} else {
				settings = self.generateEditorSettings( sectionId );
			}

			if ( ! settings ) {
				return false;
			}

			$target.addClass( 'jet-parallax-plugin-section' );
			self.generateLayouts();

			$window.on( 'scroll.jetSectionParallaxPlugin resize.jetSectionParallaxPlugin', self.scrollHandler );
			$target.on( 'mousemove.jetSectionParallaxPlugin', self.mouseMoveHandler );
			$target.on( 'mouseleave.jetSectionParallaxPlugin', self.mouseLeaveHandler );

			self.scrollUpdate();
		};

		self.generateEditorSettings = function( sectionId ) {
			var editorElements      = null,
				sectionsData        = {},
				sectionData         = {},
				sectionParallaxData = {},
				settings            = [];

			if ( ! window.elementor.hasOwnProperty( 'elements' ) ) {
				return false;
			}

			editorElements = window.elementor.elements;

			if ( ! editorElements.models ) {
				return false;
			}

			$.each( editorElements.models, function( index, obj ) {
				if ( sectionId == obj.id ) {
					sectionData = obj.attributes.settings.attributes;
				}
			} );

			if ( ! sectionData.hasOwnProperty( 'jet_parallax_plugin_layout_list' ) || 0 === Object.keys( sectionData ).length ) {
				return false;
			}

			sectionParallaxData = sectionData[ 'jet_parallax_plugin_layout_list' ].models;

			$.each( sectionParallaxData, function( index, obj ) {
				settings.push( obj.attributes );
			} );

			if ( 0 !== settings.length ) {
				return settings;
			}

			return false;
		};

		self.generateLayouts = function() {

			$( '.jet-parallax-plugin-section__layout', $target ).remove();

			$.each( settings, function( index, layout ) {
				var imageData      = layout['jet_parallax_plugin_layout_image'],
					speed          = layout['jet_parallax_plugin_layout_speed']['size'] || 50,
					zIndex         = layout['jet_parallax_plugin_layout_z_index'],
					bgSize         = layout['jet_parallax_plugin_layout_bg_size'] || 'auto',
					animProp       = layout['jet_parallax_plugin_layout_animation_prop'] || 'bgposition',
					bgX            = layout['jet_parallax_plugin_layout_bg_x'],
					bgY            = layout['jet_parallax_plugin_layout_bg_y'],
					type           = layout['jet_parallax_plugin_layout_type'] || 'none',
					_id            = layout['_id'],
					isDynamicImage = layout.hasOwnProperty( '__dynamic__' ) && layout.__dynamic__.hasOwnProperty( 'jet_parallax_plugin_layout_image' ),
					$layout        = null,
					layoutData     = {},
					safariClass    = isSafari ? ' is-safari' : '',
					macClass       = 'MacIntel' == platform ? ' is-mac' : '';

				if ( '' === imageData['url'] && ! isDynamicImage ) {
					return false;
				}

				$layout = $( '<div class="jet-parallax-plugin-section__layout elementor-repeater-item-' + _id + ' jet-parallax-plugin-section__' + type + '-layout' + macClass + '"><div class="jet-parallax-plugin-section__image"></div></div>' )
					.prependTo( $target )
					.css({
						'z-index': zIndex
					});

				var imageCSS = {
					'background-size': bgSize,
					'background-position-x': bgX + '%',
					'background-position-y': bgY + '%'
				};

				if ( '' !== imageData['url'] ) {
					imageCSS['background-image'] = 'url(' + imageData['url'] + ')';
				}

				$( '> .jet-parallax-plugin-section__image', $layout ).css( imageCSS );

				layoutData = {
					selector: $layout,
					image: imageData['url'],
					size: bgSize,
					prop: animProp,
					type: type,
					xPos: bgX,
					yPos: bgY,
					zIndex: zIndex,
					speed: 2 * ( speed / 100 )
				};

				if ( 'scroll' === type ) {
					scrollLayoutList.push( layoutData );
				}

				if ( 'mouse' === type ) {
					mouseLayoutList.push( layoutData );
				}
			});

			//$layoutList = $( '.jet-parallax-section__layout', $target );
		};

		self.scrollHandler = function( event ) {
			winScrollTop = $window.scrollTop(),
			winHeight    = $window.height();

			self.scrollUpdate();
		};

		self.scrollUpdate = function() {
			$.each( scrollLayoutList, function( index, layout ) {
				var $this      = layout.selector,
					$image     = $( '.jet-parallax-plugin-section__image', $this ),
					speed      = layout.speed,
					offsetTop  = $this.offset().top,
					thisHeight = $this.outerHeight(),
					prop       = layout.prop,
					posY       = ( winScrollTop - offsetTop + winHeight ) / thisHeight * 100;

				if ( winScrollTop < offsetTop - winHeight) posY = 0;
				if ( winScrollTop > offsetTop + thisHeight) posY = 200;

				posY = parseFloat( speed * posY ).toFixed(1);

				if ( 'bgposition' === layout.prop ) {
					$image.css( {
						'background-position-y': 'calc(' + layout.yPos + '% + ' + posY + 'px)'
					} );
				} else {
					$image.css( {
						'transform': 'translateY(' + posY + 'px)'
					} );
				}
			} );

		};

		self.mouseMoveHandler = function( event ) {
			var windowWidth  = $window.width(),
				windowHeight = $window.height(),
				cx           = Math.ceil( windowWidth / 2 ),
				cy           = Math.ceil( windowHeight / 2 ),
				dx           = event.clientX - cx,
				dy           = event.clientY - cy;

			tiltx = -1 * ( dx / cx );
			tilty = -1 * ( dy / cy);

			self.mouseMoveUpdate();
		};

		self.mouseLeaveHandler = function( event ) {
			$.each( mouseLayoutList, function( index, layout ) {
				var $this  = layout.selector,
					$image = $( '.jet-parallax-plugin-section__image', $this );

				switch( layout.prop ) {
					case 'transform3d':
						TweenMax.to(
							$image[0],
							1.5, {
								x: 0,
								y: 0,
								z: 0,
								rotationX: 0,
								rotationY: 0,
								ease:Power2.easeOut
							}
						);
					break;
				}

			} );
		}

		self.mouseMoveUpdate = function() {
			$.each( mouseLayoutList, function( index, layout ) {
				var $this  = layout.selector,
					$image = $( '.jet-parallax-plugin-section__image', $this ),
					speed  = layout.speed,
					prop   = layout.prop,
					posX   = parseFloat( tiltx * 125 * speed ).toFixed(1),
					posY   = parseFloat( tilty * 125 * speed ).toFixed(1),
					posZ   = layout.zIndex * 50,
					rotateX = parseFloat( tiltx * 25 * speed ).toFixed(1),
					rotateY = parseFloat( tilty * 25 * speed ).toFixed(1);

				switch( prop ) {
					case 'bgposition':
						TweenMax.to(
							$image[0],
							1, {
								backgroundPositionX: 'calc(' + layout.xPos + '% + ' + posX + 'px)',
								backgroundPositionY: 'calc(' + layout.yPos + '% + ' + posY + 'px)',
								ease:Power2.easeOut
							}
						);
					break;

					case 'transform':
						TweenMax.to(
							$image[0],
							1, {
								x: posX,
								y: posY,
								ease:Power2.easeOut
							}
						);
					break;

					case 'transform3d':
						TweenMax.to(
							$image[0],
							2, {
								x: posX,
								y: posY,
								z: posZ,
								rotationX: rotateY,
								rotationY: -rotateX,
								ease:Power2.easeOut
							}
						);
					break;
				}

			} );
		};

	}


}( jQuery, window.elementorFrontend ) );
