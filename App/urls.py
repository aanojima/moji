from django.conf.urls import patterns, include, url
import views, character_controller, grade_controller

urlpatterns = patterns('',
	url(r'^$', views.api),
	url(r'^character_images/(?P<unicode_value>\d+)', character_controller.character_images, name="character_images"),
	url(r'^characters/blocks/$', character_controller.character_blocks, name="character_blocks"),
	url(r'^characters/(?P<unicode_value>\d+)', character_controller.character, name='character'),
	url(r'^characters/$', character_controller.characters, name='characters'),
	url(r'^exercise/submit$', grade_controller.student_submit, name='student_submit'),

	# url(r'^scenes/resources/(?P<scene_id>\d+)', sceneplayer_controller.scene_resources, name='scene_resources'),
	# url(r'^scenes/placement/(?P<scene_id>\d+)', sceneplayer_controller.scene_placement, name='scene_placement'),
	# url(r'^scenes/(?P<scene_id>\d+)/background/set', background_controller.add_scene_background, name='add_scene_background'),
	# url(r'^scenes/(?P<scene_id>\d+)/props/add', prop_controller.add_scene_prop, name='add_scene_prop'),
	# url(r'^scenes/props/(?P<scene_prop_id>\d+)', prop_controller.scene_prop, name='scene_prop'),
	# url(r'^scenes/(?P<scene_id>\d+)', scene_controller.scene, name='scene'),
	# url(r'^scenes', scene_controller.scenes, name='scenes'),
	# url(r'^backgrounds/(?P<background_id>\d+)', background_controller.background, name='background'),
	# url(r'^backgrounds', background_controller.backgrounds, name='backgrounds'),
	# url(r'^props/(?P<prop_id>\d+)', prop_controller.prop, name='prop'),
	# url(r'^props', prop_controller.props, name='props'),
)
