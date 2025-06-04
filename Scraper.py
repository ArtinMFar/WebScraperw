import asyncio
import aiohttp
from bs4 import BeautifulSoup

BASE_URL = "https://create.roblox.com/docs"

# Full URL mappings covering tutorials, guides, and documentation sections
URL_MAPPINGS = {
    "fundamentals": {
        "overview": "/tutorials/fundamentals/",
        "variables_objects": {
            "landing": "/tutorials/fundamentals/coding-1/landing",
            "create_script": "/tutorials/fundamentals/coding-1/create-a-script",
            "object_properties": "/tutorials/fundamentals/coding-1/object-properties",
            "parents_children": "/tutorials/fundamentals/coding-1/parents-and-children"
        },
        "functions_events": {
            "landing": "/tutorials/fundamentals/coding-2/landing",
            "code_function": "/tutorials/fundamentals/coding-2/code-a-function",
            "use_parameters": "/tutorials/fundamentals/coding-2/use-information-with-parameters",
            "parameters_buttons": "/tutorials/fundamentals/coding-2/parameters-practice-buttons",
            "multiple_parameters": "/tutorials/fundamentals/coding-2/multiple-parameters-and-arguments"
        },
        "conditionals": {
            "landing": "/tutorials/fundamentals/coding-3/landing",
            "intro_if": "/tutorials/fundamentals/coding-3/intro-to-if-statements",
            "if_then_traps": "/tutorials/fundamentals/coding-3/traps-with-if-statements",
            "if_then_powerups": "/tutorials/fundamentals/coding-3/powerups-with-if-statements",
            "multiple_conditions": "/tutorials/fundamentals/coding-3/multiple-conditions",
            "else_if_points": "/tutorials/fundamentals/coding-3/give-points"
        },
        "loops": {
            "landing": "/tutorials/fundamentals/coding-4/landing",
            "while_loops": "/tutorials/fundamentals/coding-4/repeat-code-with-while-loops",
            "intro_for": "/tutorials/fundamentals/coding-4/intro-to-for-loops",
            "glow_lights": "/tutorials/fundamentals/coding-4/glow-lights-with-for-loops",
            "timed_bridge": "/tutorials/fundamentals/coding-4/timed-bridge-for-loops",
            "nest_loops": "/tutorials/fundamentals/coding-4/nest-loops"
        },
        "dictionaries_arrays": {
            "landing": "/tutorials/fundamentals/coding-5/landing",
            "intro_arrays": "/tutorials/fundamentals/coding-5/intro-to-arrays",
            "loop_arrays": "/tutorials/fundamentals/coding-5/loops-and-arrays",
            "change_arrays": "/tutorials/fundamentals/coding-5/make-changes-to-arrays",
            "intro_dictionaries": "/tutorials/fundamentals/coding-5/intro-to-dictionaries",
            "pairs_ipairs": "/tutorials/fundamentals/coding-5/pairs-and-ipairs",
            "return_values": "/tutorials/fundamentals/coding-5/return-values-from-tables"
        },
        "organize_code": {
            "landing": "/tutorials/fundamentals/coding-6/landing",
            "intro_modules": "/tutorials/fundamentals/coding-6/intro-to-module-scripts",
            "create_modules": "/tutorials/fundamentals/coding-6/create-with-module-scripts",
            "code_abstraction": "/tutorials/fundamentals/coding-6/code-abstraction",
            "code_algorithms": "/tutorials/fundamentals/coding-6/code-algorithms"
        }
    },
    "scripting": {
        "overview": "/scripting",
        "types_locations": "/scripting/locations",
        "reuse_code": "/scripting/module",
        "services": "/scripting/services",
        "properties_attributes": "/scripting/attributes",
        "events": {
            "overview": "/scripting/events",
            "deferred": "/scripting/events/deferred",
            "bindable": "/scripting/events/bindable",
            "remote": "/scripting/events/remote"
        },
        "advanced": {
            "scheduler": "/scripting/scheduler",
            "multithreading": "/scripting/multithreading",
            "native_code": "/luau/native-code-gen",
            "script_capabilities": "/scripting/capabilities",
            "security_tactics": "/scripting/security/security-tactics"
        },
        "luau_reference": {
            "overview": "/luau",
            "types": {
                "nil": "/luau/nil",
                "booleans": "/luau/booleans",
                "numbers": "/luau/numbers",
                "strings": "/luau/strings",
                "tables": "/luau/tables",
                "enums": "/luau/enums",
                "tuples": "/luau/tuples",
                "userdata": "/luau/userdata"
            },
            "data_structures": {
                "queues": "/luau/queues",
                "stacks": "/luau/stacks",
                "metatables": "/luau/metatables"
            },
            "features": {
                "comments": "/luau/comments",
                "variables": "/luau/variables",
                "scope": "/luau/scope",
                "operators": "/luau/operators",
                "control_structures": "/luau/control-structures",
                "functions": "/luau/functions",
                "type_coercion": "/luau/type-coercion",
                "type_checking": "/luau/type-checking"
            }
        }
    },
    "environment": {
        "overview": "/environment",
        "global_lighting": "/environment/global-lighting",
        "atmosphere": "/environment/atmosphere",
        "clouds": "/environment/clouds",
        "global_wind": "/environment/global-wind",
        "post_processing": "/environment/post-processing-effects",
        "skyboxes": "/environment/skyboxes"
    },
    "characters": {
        "overview": "/characters",
        "appearance": "/characters/appearance",
        "emotes": "/characters/emotes",
        "pathfinding": "/characters/pathfinding",
        "name_health": "/characters/name-and-health-display",
        "r6_r15_adapter": "/characters/r6-to-r15-adapter",
        "generate_text": "/characters/generate-text"
    },
    "players": {
        "overview": "/players",
        "teleporting": "/projects/teleport",
        "teams": "/players/teams",
        "in_experience_tools": "/players/in-experience-tools",
        "leaderboards": "/players/leaderboards",
        "loading_screens": "/players/loading-screens",
        "player_ui": {
            "avatar_editor": "/players/avatar-editor",
            "avatar_inspect": "/players/avatar-inspect-menu",
            "avatar_context": "/players/avatar-context-menu",
            "disable_default": "/players/disable-default-ui"
        }
    },
    "input": {
        "overview": "/input",
        "mouse_keyboard": "/input/mouse-and-keyboard",
        "mobile": "/input/mobile",
        "gamepad": "/input/gamepad"
    },
    "audio": {
        "overview": "/audio",
        "assets": "/audio/assets",
        "objects": "/audio/objects",
        "effects": "/audio/effects",
        "legacy": "/sound"
    },
    "ui": {
        "overview": "/ui",
        "on_screen": "/ui/on-screen-containers",
        "in_experience": "/ui/in-experience-containers",
        "ui_objects": {
            "labels": "/ui/labels",
            "buttons": "/ui/buttons",
            "frames": "/ui/frames",
            "scrolling_frames": "/ui/scrolling-frames",
            "viewport_frames": "/ui/viewport-frames",
            "video_frames": "/ui/video-frames",
            "text_input": "/ui/text-input",
            "2d_paths": "/ui/2d-paths",
            "proximity_prompts": "/ui/proximity-prompts",
            "ui_drag_detectors": "/ui/ui-drag-detectors",
            "3d_drag_detectors": "/ui/3d-drag-detectors"
        },
        "position_size": "/ui/position-and-size",
        "layout_structures": {
            "list_flex": "/ui/list-and-flex-layouts",
            "grids_tables": "/ui/grids-and-tables",
            "page_layouts": "/ui/page-layouts"
        },
        "appearance_modifiers": "/ui/appearance-modifiers",
        "size_modifiers": "/ui/size-modifiers",
        "ui_animation": "/ui/animation",
        "ui_styling": {
            "overview": "/ui/styling",
            "style_editor": "/ui/style-editor",
            "compatibility": "/ui/compatibility",
            "css_comparisons": "/ui/css-comparisons"
        },
        "nine_slice": "/ui/9-slice",
        "rich_text": "/ui/rich-text-markup",
        "text_filtering": "/ui/text-filtering"
    },
    "animation": {
        "overview": "/animation",
        "create_animations": {
            "animation_editor": "/animation/editor",
            "animation_events": "/animation/events",
            "animation_capture": "/animation/capture",
            "curve_editor": "/animation/curve-editor",
            "inverse_kinematics": "/animation/inverse-kinematics"
        },
        "use_animations": "/animation/using"
    },
    "chat": {
        "voice_chat": "/chat/voice-chat",
        "text_chat": {
            "overview": "/chat/in-experience-text-chat",
            "guidelines": "/chat/guidelines",
            "chat_window": "/chat/chat-window",
            "bubble_chat": "/chat/bubble-chat",
            "examples": {
                "chat_tags": "/chat/chat-tags",
                "proximity_chat": "/chat/proximity-chat",
                "custom_ui": "/chat/custom-ui",
                "custom_commands": "/chat/custom-commands"
            },
            "legacy_system": "/chat/legacy/legacy-chat-system"
        }
    },
    "matchmaking": {
        "overview": "/matchmaking",
        "server_scoring": "/matchmaking/server-scoring",
        "attributes_signals": "/matchmaking/attributes-and-signals",
        "customize_config": "/matchmaking/customize-configuration",
        "analytics": "/matchmaking/analytics",
        "glossary": "/matchmaking/glossary"
    },
    "performance": {
        "overview": "/performance-optimization",
        "design_performance": "/performance-optimization/design",
        "identify_issues": "/performance-optimization/identify",
        "improve_performance": "/performance-optimization/improve",
        "monitor_performance": "/performance-optimization/monitor"
    },
    "cloud_services": {
        "data_vs_memory": "/cloud-services/data-vs-memory",
        "data_stores": {
            "overview": "/cloud-services/data-stores",
            "data_stores_manager": "/cloud-services/data-stores/data-stores-manager",
            "versioning_listing": "/cloud-services/data-stores/versioning-listing-and-caching",
            "error_codes": "/cloud-services/data-stores/error-codes-and-limits",
            "observability": "/cloud-services/data-stores/observability",
            "best_practices": "/cloud-services/data-stores/best-practices",
            "implement_systems": "/cloud-services/data-stores/implement-systems"
        },
        "memory_stores": {
            "overview": "/cloud-services/memory-stores",
            "sorted_map": "/cloud-services/memory-stores/sorted-map",
            "queue": "/cloud-services/memory-stores/queue",
            "hash_map": "/cloud-services/memory-stores/hash-map",
            "observability": "/cloud-services/memory-stores/observability",
            "per_partition_limits": "/cloud-services/memory-stores/per-partition-limits",
            "best_practices": "/cloud-services/memory-stores/best-practices"
        },
        "secrets_stores": "/cloud-services/secrets-stores",
        "cross_server": "/cloud-services/cross-server-communication"
    },
    "developer_guides": {
        "unity_developers": "/roblox-for-unity-developers",
        "unreal_developers": "/roblox-for-unreal-developers"
    },
    "projects": {
        "overview": "/projects",
        "architecture": {
            "data_model": "/projects/data-model",
            "client_server": "/projects/client-server",
            "instance_streaming": "/workspace/streaming"
        },
        "manage": {
            "experiences_places": "/projects/experiences-and-places",
            "ownership_transfer": "/projects/ownership-transfer",
            "transfer_animations": "/projects/transfer-animations"
        },
        "work_in_teams": {
            "groups": "/projects/groups",
            "collaboration": "/projects/collaboration"
        },
        "activity_history": "/projects/activity-history",
        "external_tools": "/projects/external-tools",
        "place_files": "/projects/place-files"
    },
    "workspace": {
        "overview": "/workspace",
        "parts": {
            "overview": "/parts",
            "solid_modeling": "/parts/solid-modeling",
            "textures_decals": "/parts/textures-and-decals"
        },
        "meshes": "/parts/meshes",
        "models": "/parts/models",
        "materials": "/parts/materials",
        "terrain": "/parts/terrain",
        "physics": {
            "overview": "/physics",
            "assemblies": "/physics/assemblies",
            "network_ownership": "/physics/network-ownership",
            "mechanical_constraints": {
                "overview": "/physics/mechanical-constraints",
                "ball_socket": "/physics/constraints/ball-socket",
                "hinge": "/physics/constraints/hinge",
                "prismatic": "/physics/constraints/prismatic",
                "cylindrical": "/physics/constraints/cylindrical",
                "spring": "/physics/constraints/spring",
                "torsion_spring": "/physics/constraints/torsion-spring",
                "universal": "/physics/constraints/universal",
                "rope": "/physics/constraints/rope",
                "rod": "/physics/constraints/rod",
                "plane": "/physics/constraints/plane",
                "weld": "/physics/constraints/weld",
                "rigid": "/physics/constraints/rigid",
                "no_collision": "/physics/constraints/no-collision"
            },
            "mover_constraints": {
                "overview": "/physics/mover-constraints",
                "linear_velocity": "/physics/constraints/linear-velocity",
                "angular_velocity": "/physics/constraints/angular-velocity",
                "align_position": "/physics/constraints/align-position",
                "align_orientation": "/physics/constraints/align-orientation",
                "vector_force": "/physics/constraints/vector-force",
                "torque": "/physics/constraints/torque",
                "line_force": "/physics/constraints/line-force"
            },
            "sleep_system": "/physics/sleep-system",
            "adaptive_timestepping": "/physics/adaptive-timestepping",
            "character_controllers": "/physics/character-controllers",
            "roblox_units": "/physics/units"
        },
        "effects": {
            "overview": "/effects",
            "light_sources": "/effects/light-sources",
            "particle_emitters": "/effects/particle-emitters",
            "beams": "/effects/beams",
            "trails": "/effects/trails",
            "highlighting": "/effects/highlighting"
        },
        "camera": "/workspace/camera",
        "spatial_data": {
            "cframes": "/workspace/cframes",
            "collisions": "/workspace/collisions",
            "raycasting": "/workspace/raycasting"
        }
    }
}

# Content from Paste.txt embedded directly in the script
ENGINE_REFERENCE_CONTENT = """
Classes
Accessory
AccessoryDescription
Accoutrement
Actor
AdGui
AdPortal
AdService
AdvancedDragger
AirController
AlignOrientation
AlignPosition
AnalyticsService
AngularVelocity
Animation
AnimationClip
AnimationClipProvider
AnimationConstraint
AnimationController
AnimationFromVideoCreatorService
AnimationRigData
AnimationTrack
Animator
Annotation
ArcHandles
AssetDeliveryProxy
AssetPatchSettings
AssetService
Atmosphere
AtmosphereSensor
Attachment
AudioAnalyzer
AudioChannelMixer
AudioChannelSplitter
AudioChorus
AudioCompressor
AudioDeviceInput
AudioDeviceOutput
AudioDistortion
AudioEcho
AudioEmitter
AudioEqualizer
AudioFader
AudioFilter
AudioFlanger
AudioLimiter
AudioListener
AudioPages
AudioPitchShifter
AudioPlayer
AudioRecorder
AudioReverb
AudioSearchParams
AudioTextToSpeech
AvatarCreationService
AvatarEditorService
Backpack
BackpackItem
BadgeService
BallSocketConstraint
BanHistoryPages
BasePart
BasePlayerGui
BaseRemoteEvent
BaseScript
BaseWrap
Beam
BevelMesh
BillboardGui
BinaryStringValue
BindableEvent
BindableFunction
BlockMesh
BloomEffect
BlurEffect
BodyAngularVelocity
BodyColors
BodyForce
BodyGyro
BodyMover
BodyPartDescription
BodyPosition
BodyThrust
BodyVelocity
Bone
BoolValue
BoxHandleAdornment
BrickColorValue
BrowserService
BubbleChatConfiguration
BubbleChatMessageProperties
BuoyancySensor
CacheableContentProvider
Camera
CanvasGroup
Capture
CaptureService
CatalogPages
CFrameValue
ChangeHistoryService
ChannelTabsConfiguration
CharacterAppearance
CharacterMesh
Chat
ChatInputBarConfiguration
ChatWindowConfiguration
ChatWindowMessageProperties
ChorusSoundEffect
ClickDetector
ClientReplicator
ClimbController
Clothing
Clouds
ClusterPacketCache
CollectionService
Color3Value
ColorCorrectionEffect
ColorGradingEffect
CommandService
CommerceService
CompressorSoundEffect
ConeHandleAdornment
ConfigService
ConfigSnapshot
Configuration
ConfigureServerService
Constraint
ContentProvider
ContextActionService
Controller
ControllerBase
ControllerManager
ControllerPartSensor
ControllerSensor
ControllerService
CookiesService
CoreGui
CoreScriptDebuggingManagerHelper
CornerWedgePart
CreatorStoreService
CurveAnimation
CustomEvent
CustomEventReceiver
CustomLog
CylinderHandleAdornment
CylinderMesh
CylindricalConstraint
DataModel
DataModelMesh
DataModelSession
DataStore
DataStoreGetOptions
DataStoreIncrementOptions
DataStoreInfo
DataStoreKey
DataStoreKeyInfo
DataStoreKeyPages
DataStoreListingPages
DataStoreObjectVersionInfo
DataStoreOptions
DataStorePages
DataStoreService
DataStoreSetOptions
DataStoreVersionPages
Debris
DebugSettings
Decal
DepthOfFieldEffect
Dialog
DialogChoice
DistortionSoundEffect
DockWidgetPluginGui
DoubleConstrainedValue
DraftsService
DragDetector
Dragger
DraggerService
DynamicRotate
EchoSoundEffect
EditableImage
EditableMesh
EmotesPages
EqualizerSoundEffect
EulerRotationCurve
ExperienceInviteOptions
ExperienceNotificationService
Explosion
FaceControls
FaceInstance
Feature
FeatureRestrictionManager
File
FileMesh
Fire
Flag
FlagStand
FlagStandService
FlangeSoundEffect
FloatCurve
FloorWire
FluidForceSensor
Folder
ForceField
FormFactorPart
Frame
FriendPages
FriendService
FunctionalTest
GamepadService
GamePassService
GameSettings
GenerationService
GenericChallengeService
GenericSettings
Geometry
GeometryService
GetTextBoundsParams
GlobalDataStore
GlobalSettings
Glue
GroundController
GroupService
GuiBase
GuiBase2d
GuiBase3d
GuiButton
GuidRegistryService
GuiLabel
GuiMain
GuiObject
GuiService
HandleAdornment
Handles
HandlesBase
HandRigDescription
HapticEffect
HapticService
Hat
HeapProfilerService
HeightmapImporterService
HiddenSurfaceRemovalAsset
Highlight
HingeConstraint
Hint
Hole
Hopper
HopperBin
HSRDataContentProvider
HttpRbxApiService
HttpService
Humanoid
HumanoidController
HumanoidDescription
HumanoidRigDescription
IKControl
ILegacyStudioBridge
ImageButton
ImageHandleAdornment
ImageLabel
IncrementalPatchBuilder
InputAction
InputBinding
InputContext
InputObject
InsertService
Instance
InstanceAdornment
IntConstrainedValue
IntersectOperation
IntValue
InventoryPages
JointInstance
JointsService
KeyboardService
Keyframe
KeyframeMarker
KeyframeSequence
KeyframeSequenceProvider
LayerCollector
Light
Lighting
LinearVelocity
LineForce
LineHandleAdornment
LocalizationService
LocalizationTable
LocalScript
LoginService
LogService
LuaSettings
LuaSourceContainer
LuaWebService
ManualGlue
ManualSurfaceJointInstance
ManualWeld
MarkerCurve
MarketplaceService
MatchmakingService
MaterialService
MaterialVariant
MemoryStoreHashMap
MemoryStoreHashMapPages
MemoryStoreQueue
MemoryStoreService
MemoryStoreSortedMap
MemStorageConnection
MemStorageService
MeshContentProvider
MeshPart
Message
MessagingService
Model
ModuleScript
Motor
Motor6D
MotorFeature
Mouse
MouseService
MultipleDocumentInterfaceInstance
NegateOperation
NetworkClient
NetworkMarker
NetworkPeer
NetworkReplicator
NetworkServer
NetworkSettings
NoCollisionConstraint
NotificationService
NumberPose
NumberValue
Object
ObjectValue
OpenCloudApiV1
OpenCloudService
OrderedDataStore
OutfitPages
PackageLink
PackageService
Pages
Pants
Part
PartAdornment
ParticleEmitter
PartOperation
PartOperationAsset
PatchBundlerFileWatch
PatchMapping
Path
Path2D
PathfindingLink
PathfindingModifier
PathfindingService
PermissionsService
PhysicsService
PhysicsSettings
PitchShiftSoundEffect
PlacesService
Plane
PlaneConstraint
Platform
Player
PlayerGui
PlayerMouse
Players
PlayerScripts
PlayerViewService
Plugin
PluginAction
PluginCapabilities
PluginDebugService
PluginDragEvent
PluginGui
PluginGuiService
PluginManagementService
PluginManager
PluginManagerInterface
PluginMenu
PluginMouse
PluginToolbar
PluginToolbarButton
PointLight
PointsService
PolicyService
Pose
PoseBase
PostEffect
PrismaticConstraint
ProcessInstancePhysicsService
ProximityPrompt
ProximityPromptService
PublishService
PVAdornment
PVInstance
QWidgetPluginGui
RayValue
ReflectionMetadata
ReflectionMetadataCallbacks
ReflectionMetadataClass
ReflectionMetadataClasses
ReflectionMetadataEnum
ReflectionMetadataEnumItem
ReflectionMetadataEnums
ReflectionMetadataEvents
ReflectionMetadataFunctions
ReflectionMetadataItem
ReflectionMetadataMember
ReflectionMetadataProperties
ReflectionMetadataYieldFunctions
ReflectionService
RemoteDebuggerServer
RemoteEvent
RemoteFunction
RenderingTest
RenderSettings
ReplicatedFirst
ReplicatedStorage
ReverbSoundEffect
RigidConstraint
RocketPropulsion
RodConstraint
RopeConstraint
Rotate
RotateP
RotateV
RotationCurve
RunningAverageItemDouble
RunningAverageItemInt
RunningAverageTimeIntervalItem
RunService
ScreenGui
ScreenshotCapture
ScreenshotHud
Script
ScriptBuilder
ScriptContext
ScriptDocument
ScriptEditorService
ScriptProfilerService
ScriptService
ScrollingFrame
Seat
Selection
SelectionBox
SelectionHighlightManager
SelectionLasso
SelectionPartLasso
SelectionPointLasso
SelectionSphere
SensorBase
SerializationService
ServerReplicator
ServerScriptService
ServerStorage
ServiceProvider
ServiceVisibilityService
SharedTableRegistry
Shirt
ShirtGraphic
SkateboardController
SkateboardPlatform
Skin
Sky
SlidingBallConstraint
SlimContentProvider
Smoke
SmoothVoxelsUpgraderService
Snap
SocialService
SolidModelContentProvider
Sound
SoundEffect
SoundGroup
SoundService
Sparkles
SpawnerService
SpawnLocation
SpecialMesh
SphereHandleAdornment
SpotLight
SpringConstraint
StandalonePluginScripts
StandardPages
StarterCharacterScripts
StarterGear
StarterGui
StarterPack
StarterPlayer
StarterPlayerScripts
StartupMessageService
Stats
StatsItem
Status
StopWatchReporter
StringValue
Studio
StudioService
StudioTheme
StyleBase
StyleDerive
StyleLink
StyleRule
StyleSheet
SunRaysEffect
SurfaceAppearance
SurfaceGui
SurfaceGuiBase
SurfaceLight
SurfaceSelection
SwimController
SyncScriptBuilder
TaskScheduler
Team
TeamCreateData
TeamCreateService
Teams
TeleportAsyncResult
TeleportOptions
TeleportService
Terrain
TerrainDetail
TerrainIterateOperation
TerrainModifyOperation
TerrainReadOperation
TerrainRegion
TerrainWriteOperation
TestService
TextBox
TextBoxService
TextButton
TextChannel
TextChatCommand
TextChatConfigurations
TextChatMessage
TextChatMessageProperties
TextChatService
TextFilterResult
TextFilterTranslatedResult
TextLabel
TextService
TextSource
Texture
TimerService
Tool
Torque
TorsionSpringConstraint
TotalCountTimeIntervalItem
TouchInputService
TouchTransmitter
Trail
Translator
TremoloSoundEffect
TriangleMeshPart
TrussPart
Tween
TweenBase
TweenService
UGCValidationService
UIAspectRatioConstraint
UIBase
UIComponent
UIConstraint
UICorner
UIDragDetector
UIFlexItem
UIGradient
UIGridLayout
UIGridStyleLayout
UILayout
UIListLayout
UIPadding
UIPageLayout
UIScale
UISizeConstraint
UIStroke
UITableLayout
UITextSizeConstraint
UnionOperation
UniversalConstraint
UnreliableRemoteEvent
UserGameSettings
UserInputService
UserService
UserSettings
ValueBase
Vector3Curve
Vector3Value
VectorForce
VehicleController
VehicleSeat
VelocityMotor
VideoCapture
VideoCaptureService
VideoDisplay
VideoFrame
VideoPlayer
VideoService
ViewportFrame
VirtualInputManager
VirtualUser
VisibilityCheckDispatcher
Visit
VisualizationMode
VisualizationModeCategory
VisualizationModeService
VoiceChatService
VRService
VRStatusService
WedgePart
Weld
WeldConstraint
Wire
WireframeHandleAdornment
Workspace
WorkspaceAnnotation
WorldModel
WorldRoot
WrapDeformer
WrapLayer
WrapTarget
Data Types
Axes
BrickColor
CatalogSearchParams
CFrame
Color3
ColorSequence
ColorSequenceKeypoint
Content
DateTime
DockWidgetPluginGuiInfo
Enum
EnumItem
Enums
Faces
FloatCurveKey
Font
Instance
NumberRange
NumberSequence
NumberSequenceKeypoint
OverlapParams
Path2DControlPoint
PathWaypoint
PhysicalProperties
Random
Ray
RaycastParams
RaycastResult
RBXScriptConnection
RBXScriptSignal
Rect
Region3
Region3int16
RotationCurveKey
Secret
SharedTable
TweenInfo
UDim
UDim2
Vector2
Vector2int16
Vector3
Vector3int16
Enums
AccessModifierType
AccessoryType
ActionOnAutoResumeSync
ActionOnStopSync
ActionType
ActuatorRelativeTo
ActuatorType
AdAvailabilityResult
AdEventType
AdFormat
AdornCullingMode
AdShape
AdTeleportMethod
AdUIEventType
AdUIType
AdUnitStatus
AlignType
AlphaMode
AnalyticsCustomFieldKeys
AnalyticsEconomyAction
AnalyticsEconomyFlowType
AnalyticsEconomyTransactionType
AnalyticsLogLevel
AnalyticsProgressionStatus
AnalyticsProgressionType
AnimationClipFromVideoStatus
AnimationPriority
AnimatorRetargetingMode
AnnotationEditingMode
AnnotationRequestStatus
AnnotationRequestType
AppLifecycleManagerState
ApplyStrokeMode
AppShellActionType
AppShellFeature
AppUpdateStatus
AspectType
AssetCreatorType
AssetFetchStatus
AssetType
AssetTypeVerification
AudioApiRollout
AudioCaptureMode
AudioChannelLayout
AudioFilterType
AudioSimulationFidelity
AudioSubType
AudioWindowSize
AutoIndentRule
AutomaticSize
AvatarAssetType
AvatarChatServiceFeature
AvatarContextMenuOption
AvatarItemType
AvatarPromptResult
AvatarSettingsAccessoryLimitMethod
AvatarSettingsAccessoryMode
AvatarSettingsAnimationClipsMode
AvatarSettingsAnimationPacksMode
AvatarSettingsAppearanceMode
AvatarSettingsBuildMode
AvatarSettingsClothingMode
AvatarSettingsCollisionMode
AvatarSettingsCustomAccessoryMode
AvatarSettingsCustomBodyType
AvatarSettingsCustomClothingMode
AvatarSettingsHitAndTouchDetectionMode
AvatarSettingsJumpMode
AvatarSettingsLegacyCollisionMode
AvatarSettingsScaleMode
AvatarThumbnailCustomizationType
AvatarUnificationMode
Axis
BenefitType
BinType
BodyPart
BodyPartR15
BorderMode
BreakpointRemoveReason
BreakReason
BulkMoveMode
BundleType
Button
ButtonStyle
CageType
CameraMode
CameraPanMode
CameraSpeedAdjustBinding
CameraType
CaptureType
CatalogCategoryFilter
CatalogSortAggregation
CatalogSortType
CellBlock
CellMaterial
CellOrientation
CenterDialogType
CharacterControlMode
ChatCallbackType
ChatColor
ChatMode
ChatPrivacyMode
ChatRestrictionStatus
ChatStyle
ChatVersion
ClientAnimatorThrottlingMode
CloseReason
CollaboratorStatus
CollisionFidelity
CommandPermission
CompileTarget
CompletionAcceptanceBehavior
CompletionItemKind
CompletionItemTag
CompletionTriggerKind
ComputerCameraMovementMode
ComputerMovementMode
ConfigSnapshotErrorState
ConnectionError
ConnectionState
ContentSourceType
ContextActionPriority
ContextActionResult
ControlMode
CoreGuiType
CreateAssetResult
CreateOutfitFailure
CreatorType
CreatorTypeFilter
CurrencyType
CustomCameraMode
DataStoreRequestType
DebuggerEndReason
DebuggerExceptionBreakMode
DebuggerFrameType
DebuggerPauseReason
DebuggerStatus
DevCameraOcclusionMode
DevComputerCameraMovementMode
DevComputerMovementMode
DeveloperMemoryTag
DeviceFeatureType
DeviceForm
DeviceLevel
DeviceType
DevTouchCameraMovementMode
DevTouchMovementMode
DialogBehaviorType
DialogPurpose
DialogTone
DominantAxis
DraftStatusCode
DragDetectorDragStyle
DragDetectorPermissionPolicy
DragDetectorResponseStyle
DraggerCoordinateSpace
DraggerMovementMode
DraggingScrollBar
EasingDirection
EasingStyle
ElasticBehavior
EnviromentalPhysicsThrottle
ExperienceAuthScope
ExplosionType
FacialAgeEstimationResultType
FacialAnimationStreamingState
FacsActionUnit
FACSDataLod
FeedRankingScoreType
FieldOfViewMode
FillDirection
FilterErrorType
FilterResult
FinishRecordingOperation
FluidFidelity
FluidForces
Font
FontSize
FontStyle
FontWeight
ForceLimitMode
FormFactor
FramerateManagerMode
FrameStyle
FriendRequestEvent
FriendStatus
FunctionalTestResult
GameAvatarType
GamepadType
GearGenreSetting
GearType
Genre
GraphicsMode
GraphicsOptimizationMode
GuiState
GuiType
HandlesStyle
HandRigDescriptionSide
HapticEffectType
HighlightDepthMode
HorizontalAlignment
HoverAnimateSpeed
HttpCachePolicy
HttpCompression
HttpContentType
HttpError
HttpRequestType
HumanoidCollisionType
HumanoidDisplayDistanceType
HumanoidHealthDisplayType
HumanoidRigType
HumanoidStateType
IKCollisionsMode
IKControlConstraintSupport
IKControlType
ImageAlphaType
ImageCombineType
InfoType
InitialDockState
InOut
InputActionType
InputType
IntermediateMeshGenerationResult
InterpolationThrottlingMode
InviteState
ItemLineAlignment
IXPLoadingStatus
JoinSource
JointCreationMode
KeyCode
KeyInterpolationMode
KeywordFilterType
Language
LeftRight
LexemeType
LightingStyle
Limb
LineJoinMode
ListDisplayMode
ListenerLocation
ListenerType
LiveEditingAtomicUpdateResponse
LiveEditingBroadcastMessageType
LoadCharacterLayeredClothing
LoadDynamicHeads
LocationType
MarketplaceBulkPurchasePromptStatus
MarketplaceItemPurchaseStatus
MarketplaceProductType
MarkupKind
MatchmakingType
Material
MaterialPattern
MembershipType
MeshPartDetailLevel
MeshPartHeadsAndAccessories
MeshScaleUnit
MeshType
MessageType
ModelLevelOfDetail
ModelStreamingBehavior
ModelStreamingMode
ModerationStatus
ModifierKey
MouseBehavior
MoverConstraintRootBehaviorMode
MoveState
MuteState
NameOcclusion
NegateOperationHiddenHistory
NetworkOwnership
NetworkStatus
NoiseType
NormalId
NotificationButtonType
OperationType
OrientationAlignmentMode
OutfitSource
OutfitType
OutputLayoutMode
OverrideMouseIconBehavior
PackagePermission
ParticleEmitterShape
ParticleEmitterShapeInOut
ParticleEmitterShapeStyle
ParticleFlipbookLayout
ParticleFlipbookMode
ParticleFlipbookTextureCompatible
ParticleOrientation
PartType
PathfindingUseImprovedSearch
PathStatus
PathWaypointAction
PermissionLevelShown
PhysicsSimulationRate
PhysicsSteppingMethod
Platform
PlaybackState
PlayerActions
PlayerCharacterDestroyBehavior
PlayerChatType
PlayerDataErrorState
PlayerDataLoadFailureBehavior
PoseEasingDirection
PoseEasingStyle
PositionAlignmentMode
PreferredInput
PreferredTextSize
PrimalPhysicsSolver
PrimitiveType
PrivilegeType
ProductLocationRestriction
ProductPurchaseChannel
ProductPurchaseDecision
PromptCreateAssetResult
PromptCreateAvatarResult
PromptPublishAssetResult
PropertyStatus
ProximityPromptExclusivity
ProximityPromptInputType
ProximityPromptStyle
QualityLevel
R15CollisionType
RaycastFilterType
RejectCharacterDeletions
RenderFidelity
RenderingCacheOptimizationMode
RenderingTestComparisonMethod
RenderPriority
ReplicateInstanceDestroySetting
ResamplerMode
ReservedHighlightId
RestPose
ReturnKeyType
ReverbType
RibbonTool
RigScale
RigType
RollOffMode
RolloutState
RotationOrder
RotationType
RtlTextSupport
RunContext
RunState
RuntimeUndoBehavior
SafeAreaCompatibility
SalesTypeFilter
SandboxedInstanceMode
SaveAvatarThumbnailCustomizationFailure
SavedQualitySetting
SaveFilter
ScaleType
ScopeCheckResult
ScreenInsets
ScreenOrientation
ScrollBarInset
ScrollingDirection
SecurityCapability
SelectionBehavior
SelectionRenderMode
SelfViewPosition
SensorMode
SensorUpdateType
ServerLiveEditingMode
ServiceVisibility
Severity
ShowAdResult
SignalBehavior
SizeConstraint
SolverConvergenceMetricType
SolverConvergenceVisualizationMode
SortDirection
SortOrder
SpecialKey
StartCorner
StateObjectFieldType
Status
StreamingIntegrityMode
StreamingPauseMode
StreamOutBehavior
StudioCloseMode
StudioDataModelType
StudioPlaceUpdateFailureReason
StudioScriptEditorColorCategories
StudioScriptEditorColorPresets
StudioStyleGuideColor
StudioStyleGuideModifier
Style
SubscriptionExpirationReason
SubscriptionPaymentStatus
SubscriptionPeriod
SubscriptionState
SurfaceConstraint
SurfaceGuiShape
SurfaceGuiSizingMode
SurfaceType
SwipeDirection
SystemThemeValue
TableMajorAxis
TeamCreateErrorState
Technology
TeleportMethod
TeleportResult
TeleportState
TeleportType
TerrainAcquisitionMethod
TerrainFace
TextChatMessageStatus
TextDirection
TextFilterContext
TextInputType
TextTruncate
TextureMode
TextureQueryType
TextXAlignment
TextYAlignment
ThreadPoolConfig
ThrottlingPriority
ThumbnailSize
ThumbnailType
TickCountSampleMethod
TonemapperPreset
TopBottom
TouchCameraMovementMode
TouchMovementMode
TrackerError
TrackerExtrapolationFlagMode
TrackerFaceTrackingStatus
TrackerLodFlagMode
TrackerLodValueMode
TrackerMode
TrackerPromptEvent
TrackerType
TriStateBoolean
TweenStatus
UICaptureMode
UIDragDetectorBoundingBehavior
UIDragDetectorDragRelativity
UIDragDetectorDragSpace
UIDragDetectorDragStyle
UIDragDetectorResponseStyle
UIDragSpeedAxisMapping
UIFlexAlignment
UIFlexMode
UiMessageType
UITheme
UsageContext
UserCFrame
UserInputState
UserInputType
VelocityConstraintMode
VerticalAlignment
VerticalScrollBarPosition
VibrationMotor
VideoCaptureResult
VideoDeviceCaptureQuality
VideoError
ViewMode
VirtualCursorMode
VirtualInputMode
VoiceChatDistanceAttenuationType
VoiceChatState
VoiceControlPath
VolumetricAudio
VRComfortSetting
VRControllerModelMode
VRDeviceType
VRLaserPointerMode
VRSafetyBubbleMode
VRScaling
VRSessionState
VRTouchpad
VRTouchpadMode
WaterDirection
WaterForce
WebSocketState
WeldConstraintPreserve
WhisperChatPrivacyMode
WrapLayerAutoSkin
WrapLayerDebugMode
WrapTargetDebugMode
ZIndexBehavior
Globals
Lua Globals
Roblox Globals
Libraries
bit32
buffer
coroutine
debug
math
os
string
table
task
utf8
vector
"""


def parse_reference_content(content: str = ENGINE_REFERENCE_CONTENT):
    """Parse embedded engine reference content."""
    sections = {}
    current = None
    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        if line in ["Classes", "Data Types", "Enums", "Globals", "Libraries"]:
            current = line
            sections[current] = []
        elif current:
            sections[current].append(line)
    return sections


def generate_urls():
    """Generate all URLs from the mapping and the engine reference lists."""
    urls = []

    def extract_urls(data):
        if isinstance(data, dict):
            for value in data.values():
                extract_urls(value)
        elif isinstance(data, str):
            urls.append(BASE_URL + value)

    extract_urls(URL_MAPPINGS)

    refs = parse_reference_content()
    base = f"{BASE_URL}/reference/engine"
    urls.append(base)
    for section, names in refs.items():
        slug = section.lower().replace(" ", "")
        urls.append(f"{base}/{slug}")
        for name in names:
            name_slug = name.replace(" ", "")
            urls.append(f"{base}/{slug}/{name_slug}")

    return urls


async def fetch_page(session: aiohttp.ClientSession, url: str) -> str:
    """Fetch a single page and return plain text."""
    try:
        async with session.get(url) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                for script in soup(["script", "style"]):
                    script.decompose()
                text = "\n".join(t.strip() for t in soup.get_text().splitlines() if t.strip())
                return f"\n{'='*80}\nURL: {url}\n{'='*80}\n\n{text}"
            return f"\nError fetching {url}: Status {response.status}\n"
    except Exception as e:
        return f"\nError fetching {url}: {e}\n"


async def scrape_all_pages():
    """Scrape all documentation pages concurrently."""
    urls = generate_urls()
    headers = {"User-Agent": "Mozilla/5.0"}
    connector = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=connector, headers=headers) as session:
        tasks = [fetch_page(session, url) for url in urls]
        results = []
        for i in range(0, len(tasks), 10):
            batch = tasks[i : i + 10]
            results.extend(await asyncio.gather(*batch))
            print(f"Progress: {min(i+10, len(tasks))}/{len(tasks)}")
    with open("RobloxDocs_Complete.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(results))
    print(f"Total pages scraped: {len(urls)}")


def main():
    """Entry point to run the scraper."""
    print("Roblox Documentation Scraper - Complete Edition")
    print("=" * 50)
    print(
        "\nThis will scrape ALL Roblox documentation sections including tutorials,\n"
        "scripting guides, environment reference, engine API reference, and more.\n"
        "Note: scraping may take a while due to the large number of pages."
    )
    asyncio.run(scrape_all_pages())


if __name__ == "__main__":
    main()
